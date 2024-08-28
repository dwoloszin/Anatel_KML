import CalcDistAzim
import pandas as pd
import os
import sys
import ImportDF
import numpy as np




def process(Operator):
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    zip_directory = os.path.join(script_dir, 'export')
    frameSI = ImportDF.ImportDFFromZip(zip_directory)
    unique_values = frameSI['CodMunicipio'].unique().tolist()
    frameSI = frameSI.loc[frameSI['NomeEntidade'] == Operator]
    unique_values = frameSI['CodMunicipio'].unique().tolist()
    #print(unique_values,len(unique_values))
    for i in unique_values:
        frameSI2 = frameSI.loc[frameSI['CodMunicipio'] == i]
        for index, row in frameSI2.iterrows():
            latA = float(row['Latitude'].split('|')[0])
            lonA = float(row['Longitude'].split('|')[0])
            lowDista = np.inf
            for index2, row2 in frameSI2.iterrows():
                latB = float(row2['Latitude'].split('|')[0])
                lonB = float(row2['Longitude'].split('|')[0])
                distance = CalcDistAzim.CalcDist(latA,lonA,latB,lonB)
                if (distance < lowDista) and distance > 0:
                    lowDista = distance
            frameSI2.at[index,'distance'] = lowDista/2
        csv_path = os.path.join(script_dir, 'Distance')
    
        csv_path = os.path.join(csv_path,Operator + '_' + str(row['CodMunicipio']) + '.csv')
        #frameSI2.to_csv(csv_path, sep=',',encoding='ANSI', index=False)  # Save DataFrame as CSV
        frameSI2.to_csv(csv_path, sep=',', index=False)  # Save DataFrame as CSV    
    







