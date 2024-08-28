import logging
import logging.handlers
import os
import sys
import timeit
import time
import AnatelFiles
import ImportDF
import CleanData
import distanceT
import Csv_zip
import GOOGLE_CREATOR
import distCalc




logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    '''
    #==========================================
    #run once a month
    opList = ['TIM','CLARO','VIVO','ALGAR']
    for i in opList:
        distCalc.process(i)
    #=======================================
    '''



    
    inicioTotal = timeit.default_timer()
    #timeexport = time.strftime("%Y%m%d_")
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    csv_path = os.path.join(script_dir, 'export/'+'AnatelBase'+'.csv')
    zip_path = os.path.join(script_dir, 'export/'+'AnatelBase'+'.zip')
   
    AnatelFiles.download('SP')

    zip_directory = os.path.join(script_dir, 'downloaded_files')
    df = ImportDF.ImportDFFromZip(zip_directory)

    

    df.drop_duplicates(inplace=True, ignore_index=True)

    df = CleanData.process(df)
 

    
    
    
    df = distanceT.process(df)
    


    #df.to_csv(csv_path, sep=',',encoding='ANSI', index=False)  # Save DataFrame as CSV
    df.to_csv(csv_path, sep=',', index=False)  # Save DataFrame as CSV
    time.sleep(10)
    Csv_zip.process(csv_path)



    GOOGLE_CREATOR.process()



    fimtotal = timeit.default_timer()
    print ('duracao: %f' % round(((fimtotal - inicioTotal)/60),2) + ' min') 
    print ('\nALL_DONE!!!')




    logger.info(f'Updated!')
    

