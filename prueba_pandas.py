import pandas as pd
import os
import numpy as np

file = '03.22.22.xlsx'
def excel_to_csv(excel_path, csv_path):
    df = pd.read_excel(os.sep.join([excel_path,file]))
    modif = [(np.exp(1)**-x-1)*100 for x in df['beneficio %'].tolist()]
    df['beneficio %'] = modif
    df.to_csv(os.sep.join([csv_path,file[:-5]+'.csv']))
    

ruta = lambda x: os.path.join(os.getcwd(),'RESULTS',*x) 

if __name__ == "__main__":
    row = []
    excel_to_csv(excel_path = ruta(['todos excel','1']), csv_path = ruta(['todos csv','2']))
