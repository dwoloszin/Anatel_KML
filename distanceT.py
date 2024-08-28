import pandas as pd
import os
import sys
import ImportDF



script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')


def process(df):
    pathImport = r'/Distance'

    csv_pathTosave = os.path.join(script_dir, 'Distance_all/'+'Distance'+'.csv')
    fields = ['NumEstacao','distance']
    distance = ImportDF.ImportDF_fields(pathImport,fields)
    distance.drop_duplicates(inplace=True, ignore_index=True)
    distance.reset_index(drop=True, inplace=True)
    print(distance)
    
    distance.loc[distance['distance'].astype(float) > 0.28,['distance']] = 0.28
    distance.loc[distance['distance'].astype(float) < 0.05,['distance']] = 0.05
    #distance.to_csv(csv_pathTosave, sep=',',encoding='ANSI', index=False)  # Save DataFrame as CSV
    distance.to_csv(csv_pathTosave, sep=',', index=False)  # Save DataFrame as CSV

    df = pd.merge(df,distance, how='left',left_on=['NumEstacao'],right_on=['NumEstacao'])
    df.loc[df['distance'].isna(),['distance']] = 0.28

    return df
    
    



if __name__ == "__main__":
    print('ok')
    process()
