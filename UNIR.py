import pandas as pd
import os
import numpy as np

def unir(file_data, dir_copy):
    df =   pd.read_excel(os.sep.join([file_data,file]))
    join = pd.read_excel(os.sep.join([dir_copy,file]))
    print("{0} | TOTAL: {1}".format(file, df.shape[0] + join.shape[0]))
    df = pd.concat([df,join,], ignore_index= True)
    df.to_excel(ruta(['5',file]), index= False)

def contar(data_path, contar = 'rows' ):
    if contar == 'rows': return pd.read_excel(data_path).shape[0]
    elif contar == 'files': return len(os.listdir(os.sep.join(data_path.split(os.sep)[:-1])))

def separar(file_dir, sep = 1000):   
    file_ini = pd.read_excel(file_dir)
    file1 = file_ini.iloc[:sep][:]
    file2 = file_ini.iloc[sep:][:]
    file1.to_excel(file_dir, index=False)
    file2.to_excel(ruta(['1_join',file_dir.split(os.sep)[-1]]), index= False)
   
def excel_to_csv(excel_path, csv_path):
    df = pd.read_excel(os.sep.join([excel_path,file]))
    #modif = [(np.exp(1)**-x-1)*100 for x in df['beneficio %'].tolist()]
    #df['beneficio %'] = modif
    df.to_csv(os.sep.join([csv_path,file[:-5]+'.csv']))
    #df.to_excel(ruta(['todos excel nuevo',x,file]), index= False)


ruta = lambda x: os.path.join(os.getcwd(),'RESULTS',*x) 

if __name__ == "__main__":
    row = []
    for x in np.arange(5)+ 1:
        x = str(x)
        data = [x for x in os.listdir(ruta(['todos excel',x]))]   
        for file in data:
            # #SEPARAR
            # separar(ruta(['todos excel_antiguo',file]), sep = 1000)

            # UNIR
            # unir(file_data = ruta(['1']), dir_copy= ruta(['1_join']))

            # CONTAR
            # row.append(contar(contar = 'rows', data_path= ruta(['1',file])))
            # print(row[-1])
            excel_to_csv(excel_path = ruta(['todos excel',x]), csv_path = ruta(['todos csv',x]))
            print(f'Carpeta {str(x)} | {file} convertido.')
