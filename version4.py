import numpy
import numpy as np
from pyautocad import Autocad, APoint, aDouble
import pyautocad
import datetime
import ren
import math

startt = datetime.datetime.now()
acad = Autocad(create_if_not_exists=True)
print(acad.doc.Name)
objects = [] 
obstacles = []

for obj in acad.iter_objects():
    if obj.Layer == 'siatka':
        objects.append(obj)
    if obj.Layer == 'przeszkody':
        obstacles.append(obj)


#number of squares
zs = 30



## Generating mesh
lpo = []
LiL = numpy.linspace(objects[0].Coordinates[0:2],objects[0].Coordinates[6:],zs)
LiP = numpy.linspace(objects[0].Coordinates[2:4],objects[0].Coordinates[4:6],zs)

for i in range(0,len(LiP)):
    t = acad.model.AddLine(APoint(LiP[i][0],LiP[i][1]),APoint(LiL[i][0],LiL[i][1]))
    lpo.append(t)


lpi=[]
LiG = numpy.linspace(objects[0].Coordinates[0:2],objects[0].Coordinates[2:4],zs)
LiD = numpy.linspace(objects[0].Coordinates[6:],objects[0].Coordinates[4:6],zs)

nodes = []
for i in range(0,len(LiD)):
    t = acad.model.AddLine(APoint(LiG[i][0],LiG[i][1]),APoint(LiD[i][0],LiD[i][1]))
    lpi.append(t)
for elements in lpo:
    for lin in lpi:
        q = elements.IntersectWith(lin,0)
        nodes.append(q)





sqrs = []
for i in range(len(nodes)):
    if i +1+zs <len(nodes):
        sqr = acad.model.AddPolyline(aDouble(nodes[i][0],nodes[i][1],0,nodes[i+1][0],nodes[i+1][1],0,nodes[i+1+zs][0],nodes[i+1+zs][1],0,nodes[i+zs][0],nodes[i+zs][1],0,nodes[i][0],nodes[i][1],0))
        sqrs.append(sqr)
        sqr.Layer = 'kwadraty'
        sqr.Color = 30
    if i+1+zs > len(nodes):
        break

starto = datetime.datetime.now()

print(len(sqrs))
for i in range(zs-1,len(sqrs),zs):
    if i <= len(sqrs):
        sqrs[i].Delete()
    if i > len(sqrs):
        break


    
##nkwa == number of squares in mesh
nkwa = ren.ren(sqrs,zs)

durationn = datetime.datetime.now() - starto




num1 = []
num2 = []

#bok == length of squares side
bok = pyautocad.types.distance(nodes[0],nodes[1])


for i in range(len(lpi)-1):
    ww = lpi[i].Copy()
    ww.Move(APoint(-bok/2,0),APoint(0,0)) 
    num2.append(ww)

for i in range(len(lpo)-1):
    z = lpo[i].Copy()
    z.Move(APoint(0,-bok/2),APoint(0,0)) 
    num1.append(z)



numbers=[]
for i in range(len(num1)):
    pp = i*(zs-1)+(numpy.linspace(0,zs-1,zs))
    for j in range(len(num1)):
        en = acad.model.AddText(str(pp[j]) , APoint(num1[i].IntersectWith(num2[j],0)), bok/5)
        numbers.append(en)
print('Numbers added')
    
kwaAva = []
kwaNotAva = []

for sqrs in nkwa:
    for i in range(len(obstacles)):
        if sqrs.IntersectWith(obstacles[i],0):
            sqrs.Color = 100
            sqrs.ConstantWidth = 15

for kwa in nkwa:
    if kwa.Color == 100:
        kwaNotAva.append(kwa)
    if kwa.Color == 30:
        kwaAva.append(kwa)




start = []
metaa = []
start.append(nkwa[1])
metaa.append(nkwa[2])

cu_po = start[0]
meta = metaa[0]

pairs = []
pair = []
for i in range(zs-1):
    for j in range(zs-1):
        pair.append(j)
        pair.append(-i)
        pairs.append((j,-i))

for lines in num1:
    lines.Delete()
for lines in num2:
    lines.Delete()
  
values = list(range(len(nkwa)))    

kaipa = {}
for i in range(len(values)):
    kaipa[str(values[i])] = pairs[i]


##algorithm A*

neigh = []
opens = []
closed = []
ite = 1
GVal = {}
GVals = {}
NeighsOfKwa = {}
values = list(range(len(nkwa)))
for i in range(len(values)):
    NeighsOfKwa[str(values[i])] = []

ClosedsParent = {}
for i in range(len(values)):
    ClosedsParent[str(values[i])] = 0
WykSa = []
GVal[str(nkwa.index(cu_po))] = 0
GVals[str(nkwa.index(cu_po))] = 0
while (ite < 3000) and nkwa.index(cu_po) != nkwa.index(meta) :
    for kwa in nkwa:
        if cu_po.IntersectWith(kwa,0) and kwa is not cu_po and kwa not in kwaNotAva and kwa not in closed and kwa not in neigh and kwa not in opens:
            neigh.append(kwa)
            kwa.Color=252
            kwa.ConstantWidth = 20
            opens.append(kwa)
        if cu_po.IntersectWith(kwa,0) and kwa is not cu_po and kwa not in kwaNotAva and kwa not in closed and kwa not in WykSa:
            NeighsOfKwa[str(nkwa.index(cu_po))].append(nkwa.index(kwa))
            WykSa.append(kwa)

    if cu_po in opens:
        print('Cu_po')
    else:
        print('Not Cu_po')

    Gy=[]
    Hy=[]

    for nei in opens:
        if abs((nkwa.index(cu_po) - nkwa.index(nei))) == 1 or abs((nkwa.index(cu_po) - nkwa.index(nei))) == zs-1:
            G = 10
        else:
            G=14
        GVals[str(nkwa.index(nei))] = GVals[str(nkwa.index(cu_po))]+ G
        GVal.setdefault(str(nkwa.index(nei)),GVal[str(nkwa.index(cu_po))] + G)
        if GVals[str(nkwa.index(nei))] < GVal[str(nkwa.index(nei))]:
            GVal[str(nkwa.index(nei))] = GVals[str(nkwa.index(nei))]

        H = 10*(math.sqrt((kaipa[str(nkwa.index(nei))][0]-kaipa[str(nkwa.index(meta))][0])**2+(kaipa[str(nkwa.index(nei))][1]-kaipa[str(nkwa.index(meta))][1])**2))
        Gy.append(nkwa.index(nei))
        Gy.append(GVal[str(nkwa.index(nei))])
        Hy.append((nkwa.index(nei)))
        Hy.append(H)
    
    print('Gy',Gy)
    print('Hy',Hy)

    efy = []
    sefy = []

    for i in range(0,len(Gy),2):
        F=Gy[i+1]+Hy[i+1]-0.00001
        efy.append(Hy[i])
        efy.append(F)
        sefy.append(F)

    m = min(sefy)
    print('m',m)
    m1 = int(efy.index(m)-1)
    print('m1',m1)
    print('CUPO',nkwa.index(cu_po))
    
    if cu_po in opens:
        opens.remove(cu_po)

    closed.append(cu_po)

    for keys in NeighsOfKwa:

        for i in range(len(NeighsOfKwa[keys])):
            be = nkwa.index(nkwa[int(keys[0])])
            if nkwa.index(nkwa[efy[m1]]) in NeighsOfKwa[keys]:
                ClosedsParent[str(nkwa.index(nkwa[efy[m1]]))]=nkwa.index(nkwa[int(keys)])

    cu_po = nkwa[efy[m1]]
    if cu_po in opens:
        opens.remove(cu_po)
        
    print('index',nkwa.index(nkwa[efy[m1]]))
    cu_po.Color=10
    cu_po.ConstantWidth = 30
    ite = ite +1
    
    print('Loop transition',ite-1)
    neigh = []


for kwa in nkwa:
    if cu_po.IntersectWith(kwa,0) and kwa not in kwaNotAva and kwa is not cu_po and kwa not in closed:
        neigh.append(kwa)
        kwa.Color=252
        kwa.ConstantWidth = 20

print('List of neighbours for squares',NeighsOfKwa)
print('ParentForClosed',ClosedsParent)


road = []
iter = 0


while nkwa.index(start[0]) not in road:
    for keys in ClosedsParent:
        if iter == 0:
            keys = nkwa.index(cu_po)
            wu = nkwa.index(cu_po)
            print('This sentence should be printed literally ONE time ')
        if iter == 0:
            pu = ClosedsParent[str(keys)]
            wu = ClosedsParent[str(pu)]
            road.append(pu)
            road.append(wu)
        if keys == str(wu):
            pu = ClosedsParent[str(wu)]
            wu = ClosedsParent[str(pu)]
            road.append(pu)
            road.append(wu)
        iter = iter+1
road.append(nkwa.index(meta))
for step in road:
    nkwa[step].Color = 170
    nkwa[step].ConstantWidth = 27
    
duration = datetime.datetime.now() - startt

print('Duration:' , duration)

for elements in nkwa:
    if elements.Color != 170:
        elements.Delete()

for el in lpo:
    el.Delete()
for el in lpi:
    el.Delete()

for el in numbers:
    el.Delete()






    
    





