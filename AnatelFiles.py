import os
import sys
import shutil
import datetime
import glob
import time
from seleniumbase import Driver


tec_List = ['GSM', 'WCDMA', 'LTE', 'NR']
delayTime = 2

script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
download_directory = os.path.join(script_dir, 'downloaded_files')
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

def delete_folder_contents(folder_directory):
    try:
        # Iterate over all files and subdirectories in the folder
        for filename in os.listdir(folder_directory):
            file_path = os.path.join(folder_directory, filename)
            # Check if it's a file
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete the file
            # Check if it's a directory
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Delete the directory and its contents recursively
        print(f"All contents in {folder_directory} deleted successfully.")
    except Exception as e:
        print(f"Error deleting contents of {folder_directory}: {e}")

def get_last_updated_file(NameCheck):
    # Get list of files in the folder
    files = os.listdir(download_directory)
    if len(files) == 0:
        return True
    # Filter out directories, leaving only files
    files = [f for f in files if os.path.isfile(os.path.join(download_directory, f))]
    # Sort files by their modification time (ascending order by default)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(download_directory, x)))
    # Get the last file in the sorted list
    last_file = files[-1] if files else None  
    last_file = last_file[:-4]
    if NameCheck != last_file:
        return True
    return False





def is_file_same_date1(file_Name):
    file_path = os.path.join(download_directory, file_Name)
    if not os.path.exists(file_path):
        return True
    file_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).date()
    today_date = datetime.date.today()
    return file_date != today_date
    

def get_last_updated_file(NameCheck):
    # Get list of files in the folder
    files = os.listdir(download_directory)
    if len(files) == 0:
        return True
    # Filter out directories, leaving only files
    files = [f for f in files if os.path.isfile(os.path.join(download_directory, f))]
    # Sort files by their modification time (ascending order by default)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(download_directory, x)))
    # Get the last file in the sorted list
    last_file = files[-1] if files else None  
    last_file = last_file[:-4]
    if NameCheck != last_file:
        return True
    return False

def wait_for_downloads_to_complete(): # not working fine, try to a better aprouche
    while True:
        downloading_files = glob.glob(os.path.join(download_directory, '*.zip'))
        if len(downloading_files) > 0:
            print(downloading_files)
            break
        time.sleep(1)  # Wait for 1 second and then check again


def rename_downloaded_files(ArchiveName):
    downloaded_files = glob.glob(os.path.join(download_directory, '*.zip'))
    if downloaded_files:
        # Sort the files by modification time in descending order
        downloaded_files.sort(key=os.path.getmtime, reverse=True)
        latest_file_path = downloaded_files[0]  # Get the path of the most recent file
        custom_filename = os.path.join(download_directory, f"{ArchiveName}.zip")
        
        # Check if custom filename already exists, delete it if it does
        if os.path.exists(custom_filename):
            os.remove(custom_filename)
        
        # Rename the latest downloaded file to the custom filename
        os.rename(latest_file_path, custom_filename)
        print(f"Renamed and overwritten {latest_file_path} to {custom_filename}")
    else:
        print("No downloaded files found.")




def getAnatelData(state, tec):
    #delete_folder_contents(download_directory)
    driver = Driver()
    driver.open("http://sistemas.anatel.gov.br/se/public/view/b/licenciamento.php")
    driver.sleep(2)
    driver.click('//*[@id="tblFilter"]/span[5]')
    driver.sleep(2)
    driver.click(f"//*[@id='fc_8']/option[text()='{state}']")
    driver.sleep(5)
    driver.type('//*[@id="fc_11"]', f"{tec}\n")
    driver.sleep(5)
    driver.click('//*[@id="download_csv"]')
    #driver.click('//*[@id="download_xlsx"]')
    driver.sleep(30) # 30 for csv, 120 to xlsx
    wait_for_downloads_to_complete()
    rename_downloaded_files(tec)
    driver.quit()


def download(stade):
    for i in tec_List:
        if is_file_same_date1(i+'.zip'):
            while get_last_updated_file(i):
                getAnatelData(stade, i)


if __name__ == "__main__":

    download('SP')
    