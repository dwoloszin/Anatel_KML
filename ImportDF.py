import os
import sys
import glob
import numpy as np
import pandas as pd
from datetime import datetime
from os.path import getmtime
from zipfile import ZipFile
import shutil


def change_columnsName(df):
    for i in df.columns:
        df.rename(columns={i:i + '_' + df.name},inplace=True)
    return df

def ImportDF(pathImport):
    pathImportSI = os.getcwd() + pathImport
    all_filesSI = glob.glob(pathImportSI + "/*.csv")
    all_filesSI.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    li = []
    lastData = datetime.fromtimestamp(getmtime(all_filesSI[0])).strftime('%Y%m%d')
    for filename in all_filesSI:
        fileData = datetime.fromtimestamp(getmtime(filename)).strftime('%Y%m%d')
        iter_csv = pd.read_csv(filename, index_col=None, encoding="ANSI",header=0, on_bad_lines='skip',dtype=str, sep = ',',decimal=',',iterator=True, chunksize=10000 )
        df = pd.concat([chunk for chunk in iter_csv]) # & |  WORKS
        li.append(df)
    frameSI = pd.concat(li, axis=0, ignore_index=True)
    frameSI = frameSI.drop_duplicates()

    return frameSI


def ImportDF_fields(pathImport,fields):
    pathImportSI = os.getcwd() + pathImport
    all_filesSI = glob.glob(pathImportSI + "/*.csv")
    all_filesSI.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    li = []
    lastData = datetime.fromtimestamp(getmtime(all_filesSI[0])).strftime('%Y%m%d')
    for filename in all_filesSI:
        fileData = datetime.fromtimestamp(getmtime(filename)).strftime('%Y%m%d')
        #iter_csv = pd.read_csv(filename, index_col=None, encoding="ANSI",header=0, on_bad_lines='skip',dtype=str, sep = ',',decimal=',',iterator=True, chunksize=10000, usecols = fields )
        iter_csv = pd.read_csv(filename, index_col=None, encoding="latin1",header=0, on_bad_lines='skip',dtype=str, sep = ',',decimal=',',iterator=True, chunksize=10000, usecols = fields )
        
        df = pd.concat([chunk for chunk in iter_csv]) # & |  WORKS
  
        li.append(df)
    frameSI = pd.concat(li, axis=0, ignore_index=True)
    frameSI = frameSI.drop_duplicates()

    return frameSI




def ImportDFFromZip(zip_dir):
    # Create a temporary directory for extracted files
    temp_dir = 'temp_extracted'
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Get a list of all zip files in the directory
        zip_files = glob.glob(os.path.join(zip_dir, '*.zip'))

        li = []

        for zip_file_path in zip_files:
            # Extract all CSV files from the current zip file
            with ZipFile(zip_file_path, 'r') as zip_file:
                zip_file.extractall(temp_dir)

            # Get a list of extracted CSV files
            extracted_csv_files = glob.glob(os.path.join(temp_dir, '*.csv'))
            extracted_csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

            lastData = datetime.fromtimestamp(os.path.getmtime(extracted_csv_files[0])).strftime('%Y%m%d')

            for csv_file in extracted_csv_files:
                file_data = datetime.fromtimestamp(os.path.getmtime(csv_file)).strftime('%Y%m%d')
                iter_csv = pd.read_csv(csv_file, index_col=None, encoding="latin1", header=0, on_bad_lines='skip', dtype=str, sep=',', decimal=',', iterator=True, chunksize=10000)
                df = pd.concat([chunk for chunk in iter_csv])
                df['UpdateDate'] = file_data
                li.append(df)

            # Clean up by removing the temporary directory and its contents for each zip file
            shutil.rmtree(temp_dir, ignore_errors=True)

        frameSI = pd.concat(li, axis=0, ignore_index=True)
        frameSI = frameSI.drop_duplicates()

        return frameSI
    finally:
        # Clean up by removing the temporary directory and its contents
        shutil.rmtree(temp_dir, ignore_errors=True)

