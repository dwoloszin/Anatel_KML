import math
def CalcPointsSector(lat,lon, azi,d):
    R = 6378.1 #Radius of the Earth
    #d = 0.28 #Distance in km

    az1 = (float(azi) - (65/2)) * (math.pi/180)
    az2 = (float(azi) - (65/4)) * (math.pi/180)
    az3 = (float(azi)) * (math.pi/180)
    az4 = (float(azi) + (65/4)) * (math.pi/180)
    az5 = (float(azi) + (65/2)) * (math.pi/180)

    azimuth = []
    azimuth.append(az1)
    azimuth.append(az2)
    azimuth.append(az3)
    azimuth.append(az4)
    azimuth.append(az5)

    #lat2  52.20444 - the lat result I'm hoping for
    #lon2  0.36056 - the long result I'm hoping for.

    lat1 = math.radians(float(lat)) #Current lat point converted to radians
    lon1 = math.radians(float(lon)) #Current long point converted to radians
    
    p1 = (lon,lat)
    points = []
    points.append(p1)
    for i in azimuth:
        lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(i))

        lon2 = lon1 + math.atan2(math.sin(i)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        cord = (lon2,lat2)
        points.append(cord)
    
    points.append(p1)
    return points
     
#print (CalcPointsSector(-22.487167, -51.6615, 20))