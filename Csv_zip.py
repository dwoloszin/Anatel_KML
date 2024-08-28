import os
import sys
import zipfile

def process(csv_path):
    archiveName = csv_path.split('/')[-1]
    zip_path = csv_path[:-4]+".zip"
    # Create a ZIP archive and add the CSV file to it
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, archiveName)
    # Clean up by deleting the CSV file
    os.remove(csv_path)
    print(f'DataFrame saved as {csv_path} and compressed into {zip_path}')