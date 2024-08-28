import pyproj
from operator import itemgetter
import timeit

#Dario Woloszin

def CalcDist(latA,lonA,latB,lonB):
    #latitudeA = str(latA).replace(',','.')
    #longitudeA = str(lonA).replace(',','.')

    #latitudeB = str(latB).replace(',','.')
    #longitudeB = str(lonB).replace(',','.')
    geod = pyproj.Geod(ellps='WGS84')
    #azimuth1, azimuth2, distance = geod.inv(longitudeA, latitudeA, longitudeB, latitudeB)
    azimuth1, azimuth2, distance = geod.inv(lonA, latA, lonB, latB)
    if(azimuth1 < 0 ):
        azimuth1 = 360 + azimuth1
    if(azimuth2 < 0 ):
        azimuth2 = 360 + azimuth2

    
    #dist = str(round(distance,2)/1000).replace('.',',')
    dist = round(distance,2)/1000 # retur the distance divide by 2 in km
  
    return dist



















'''

inicio = timeit.default_timer()

base = ReadWrite.readDoc('BASE_TIM.csv')
data = ReadWrite.readDoc('Pontos.csv')
jump = 0
lista3 = []
qtosProximos = 3
lista3.append(["Pontos", "BASE_TIM","Distancia(mt)","Azim_BaseTIM->Pontos","Azim_Pontos->BaseTIM"])
geod = pyproj.Geod(ellps='WGS84')
radius = int(input("Please enter Radius(mt): "))
print ("Processing...")
for i in range(1,len(data)):
    listCalc = []
    for j in range(1,len(base)):
        tempList = []
        labelData = data[i].split(';')[0]
        labelBase = base[j].split(';')[0]
        latData = float(data[i].split(';')[1].replace(',','.'))
        lonData = float(data[i].split(';')[2].replace(',','.'))
        latBase = float(base[j].split(';')[1].replace(',','.'))
        lonBase = float(base[j].split(';')[2].replace(',','.'))
        baseCord = latBase, lonBase
        pontoCord = latData, lonData
        
        azimuth1, azimuth2, distance = geod.inv(lonData, latData, lonBase, latBase)
        if(azimuth1 < 0 ):
            azimuth1 = 360 + azimuth1
        if(azimuth2 < 0 ):
            azimuth2 = 360 + azimuth2
        #print(data[i].split(';')[0],base[j].split(';')[0], distance, azimuth1, azimuth2)
        if (distance < radius):
            tempList.append(data[i].split(';')[0])
            tempList.append(base[j].split(';')[0])
            tempList.append(distance)
            tempList.append(azimuth1)
            tempList.append(azimuth2)

            listCalc.append(tempList)
    if len(listCalc) > 0:
        listCalc = sorted(listCalc, key=itemgetter(2))
        auxTemp = []
        auxTemp.append(listCalc[0][0])
        
        for i in range(0,len(listCalc)):  
            auxTemp.append(listCalc[i][1])
            auxTemp.append(int(round(listCalc[i][2])))
            auxTemp.append(int(round(listCalc[i][3])))
            auxTemp.append(int(round(listCalc[i][4])))



        if auxTemp not in lista3:
            lista3.append(auxTemp)
            auxTemp = []
           
print ("Almost there! saving data... ")
ReadWrite.writeLine("DistanciaEntrePontos",lista3)
fim = timeit.default_timer()
print ("All done!")
print ('duracao: %f' % ((fim - inicio)/60) + ' min')
'''





