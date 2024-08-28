import pandas as pd
import numpy as np
import unique




def process(df2):
    df =df2.copy()
    Operator_List = ['TELEF','TIM','CLARO','ALGAR']
    for i in Operator_List:
        # Check if "CompanyName" contains "TELEFONICA" and replace with "VIVO"
        df.loc[df['NomeEntidade'].str.contains(i, case=False, na=False), 'NomeEntidade'] = i
    df = df[df['NomeEntidade'].isin(Operator_List)]
    df.loc[df['NomeEntidade'] == 'TELEF',['NomeEntidade']] = 'VIVO'
    df = normalizeAzimuth(df,'Azimute')
    # Extract the first part of the data before 'M' or 'k'
    #df['DesignacaoEmissao'] = df['DesignacaoEmissao'].str.extract(r'(\d+)(?=[Mk]?)')

    df.sort_values(by=['NomeEntidade','NumEstacao','physicalSector','Azimute','Tecnologia'], ascending=[True,True,True,True,True], inplace=True)
    df['Ref'] = df['NomeEntidade'].astype(str) + df['NumEstacao'].astype(str) + df['physicalSector'].astype(str)
    columnsToDrop = ['Status.state','NumServico','tipoTecnologia','meioAcesso','CodTipoClasseEstacao','CodTipoAntena','Polarizacao','CodDebitoTFI','NumRede','_id','NumFistelAssociado','NomeEntidadeAssociado']
    df.drop(columnsToDrop, axis=1, inplace=True)
    df.drop_duplicates(inplace=True, ignore_index=True)
    df.reset_index(drop=True, inplace=True)

    df['Azimute_(Median)'] = df.groupby('Ref')['Azimute'].transform('median').round(0)
    #df['Azimute_LTE-NR(Median)'] = df.loc[df['Tecnologia'].isin(['NR', 'LTE'])].groupby('Ref')['Azimute'].transform('median').round(0)

    #GroupBy convert all data str befor agg
    df = df.fillna('').groupby(['Ref'], as_index=True).agg(lambda x: '|'.join(map(str, x)))

    
    
    removefromloop = []
    locationBase_top = list(df.columns)
    res = list(set(locationBase_top)^set(removefromloop))
    
    for i in res: 
        for index, row in df.iterrows():
            df.at[index, i] = '|'.join(unique.unique_list(df.at[index, i].split('|')))  
    
    return df

def custom_conversion(value):
    try:
        return int(value)
    except ValueError:
        return 0  # Replace non-integer values with -1

def convert_to_float_or_zero(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0  # Convert non-numeric values to 0.0



def normalizeAzimuth(df2,azimuth_Column):
    df =df2.copy()
    df[azimuth_Column] = df[azimuth_Column].apply(convert_to_float_or_zero)
    df[azimuth_Column] = df[azimuth_Column].apply(custom_conversion)
    df.loc[(df[azimuth_Column] > 360) |
           (df[azimuth_Column] < 0),[azimuth_Column]] = 0

    # Define conditions and corresponding values
    conditions = [
        (df[azimuth_Column] >= 0) & (df[azimuth_Column] <= 89),
        (df[azimuth_Column] >= 90) & (df[azimuth_Column] <= 179),
        (df[azimuth_Column] >= 180) & (df[azimuth_Column] <= 269),
        (df[azimuth_Column] >= 270) & (df[azimuth_Column] <= 359)
        ]
    values = [1, 2, 3, 4]
 
    # Use np.select to assign values based on conditions
    df['physicalSector'] = np.select(conditions, values, default=0)

    return df
