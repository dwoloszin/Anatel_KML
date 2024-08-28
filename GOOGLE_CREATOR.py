import os
import sys
import glob
import numpy as np
from itertools import chain
import pandas as pd
from simplekml import Kml, ListItemType, Color, Types, Snippet
import unique
import SectorGoogle
import simplekml
import timeit
import ImportDF

def process():
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    zip_directory = os.path.join(script_dir, 'export')

    csv_path = os.path.join(script_dir, 'export/'+'GOOGLE_ALL')
    frameSI = ImportDF.ImportDFFromZip(zip_directory)
    frameSI_copy = frameSI.copy()
    frameSI_Null = frameSI_copy[~frameSI_copy['Azimute_(Median)'].astype(bool)]
    UpdateDate = frameSI['UpdateDate'][0]
    kml = Kml(name="GOOGLE_ALL_"+UpdateDate, open=1)
    screen = kml.newscreenoverlay(name='Legends')
    legend_path = os.path.join(script_dir, 'legend/'+'legend5'+'.png')
    screen.icon.href = legend_path
    screen.overlayxy = simplekml.OverlayXY(x=0,y=1,xunits=simplekml.Units.fraction,yunits=simplekml.Units.fraction)
    screen.screenxy = simplekml.ScreenXY(x=1,y=1,xunits= simplekml.Units.pixels,yunits=simplekml.Units.insetpixels)
    screen.size.x = -1
    screen.size.y = -1
    screen.size.xunits = simplekml.Units.fraction
    screen.size.yunits = simplekml.Units.fraction

    endIDlist = []
    operator = []
    for index, row in frameSI.iterrows():
        if row['NomeEntidade'] not in operator:
            fol0 = kml.newfolder(name=row['NomeEntidade'])
            operator.append(row['NomeEntidade'])

        if row['NumEstacao'] not in endIDlist:
            fol = fol0.newfolder(name=row['NumEstacao'])
            endIDlist.append(row['NumEstacao'])
        

        pol = fol.newpolygon(name=row['physicalSector'])

        lat = float(row['Latitude'].split('|')[0])
        lon = float(row['Longitude'].split('|')[0])
        az = row['Azimute_(Median)']
        distt = float(row['distance'])
        vectors = SectorGoogle.CalcPointsSector(lat,lon,az,distt)
        pol.outerboundaryis = vectors

        pol.style.linestyle.color = colorretured(row['NomeEntidade'])
        pol.style.linestyle.width = 5
        pol.style.polystyle.color = simplekml.Color.changealphaint(180, colorretured(row['NomeEntidade']))


        for i in frameSI.columns:
            pol.extendeddata.newdata(name= i, value=str(row[i]), displayname=None)
    
    kml.savekmz(csv_path + ".kmz",format=False)      
    




def colorretured(value):
    if value == 'chartreuse': return simplekml.Color.chartreuse
    if value == 'chocolate': return simplekml.Color.chocolate
    if value == 'coral': return simplekml.Color.coral
    if value == 'cornflowerblue': return simplekml.Color.cornflowerblue
    if value == 'cornsilk': return simplekml.Color.cornsilk
    if value == 'crimson': return simplekml.Color.crimson
    if value == 'cyan': return simplekml.Color.cyan
    if value == 'darkblue': return simplekml.Color.darkblue
    if value == 'darkcyan': return simplekml.Color.darkcyan
    if value == 'darkgoldenrod': return simplekml.Color.darkgoldenrod
    if value == 'darkgray': return simplekml.Color.darkgray
    if value == 'darkgreen': return simplekml.Color.darkgreen
    if value == 'darkgrey': return simplekml.Color.darkgrey
    if value == 'darkkhaki': return simplekml.Color.darkkhaki
    if value == 'darkmagenta': return simplekml.Color.darkmagenta
    if value == 'darkolivegreen': return simplekml.Color.darkolivegreen
    if value == 'darkorange': return simplekml.Color.darkorange
    if value == 'darkorchid': return simplekml.Color.darkorchid
    if value == 'darkred': return simplekml.Color.darkred
    if value == 'darksalmon': return simplekml.Color.darksalmon
    if value == 'darkseagreen': return simplekml.Color.darkseagreen
    if value == 'darkslateblue': return simplekml.Color.darkslateblue
    if value == 'darkslategray': return simplekml.Color.darkslategray
    if value == 'darkslategrey': return simplekml.Color.darkslategrey
    if value == 'darkturquoise': return simplekml.Color.darkturquoise
    if value == 'darkviolet': return simplekml.Color.darkviolet
    if value == 'deeppink': return simplekml.Color.deeppink
    if value == 'deepskyblue': return simplekml.Color.deepskyblue
    if value == 'dimgray': return simplekml.Color.dimgray
    if value == 'dimgrey': return simplekml.Color.dimgrey
    if value == 'dodgerblue': return simplekml.Color.dodgerblue
    if value == 'firebrick': return simplekml.Color.firebrick
    if value == 'floralwhite': return simplekml.Color.floralwhite
    if value == 'forestgreen': return simplekml.Color.forestgreen
    if value == 'fuchsia': return simplekml.Color.fuchsia
    if value == 'gainsboro': return simplekml.Color.gainsboro
    if value == 'ghostwhite': return simplekml.Color.ghostwhite
    if value == 'gold': return simplekml.Color.gold
    if value == 'goldenrod': return simplekml.Color.goldenrod
    if value == 'gray': return simplekml.Color.gray
    if value == 'green': return simplekml.Color.green
    if value == 'greenyellow': return simplekml.Color.greenyellow
    if value == 'grey': return simplekml.Color.grey
    if value == 'white': return simplekml.Color.white
    if value == 'black': return simplekml.Color.black
    if value == 'TIM': return simplekml.Color.darkblue
    if value == 'VIVO': return simplekml.Color.purple
    if value == 'CLARO': return simplekml.Color.red
    if value == 'ALGAR': return simplekml.Color.yellow        

