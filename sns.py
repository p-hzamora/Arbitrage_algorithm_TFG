from typing import Counter
from unittest.mock import DEFAULT
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import seaborn as sns
from arbitrage.meses import get_month
from collections import defaultdict
import re

ruta = lambda x: os.path.join(os.getcwd(),*x)


def max_beneficio(total = 5, month_letter = False, update_table = False, get_general_tab= False) -> None:
        os.chdir(os.path.join(os.getcwd(),'RESULTS'))
        files = os.listdir(ruta(['todos csv','1']))
        names = [x[:-7] for x in files]
        maximos = []
        df_max_values = pd.DataFrame()
        list_unic = []

        for j in np.arange(total)+1:
                dicc = {}
                maximo = []
                data = {
                        r'days': [],
                        r't': [],
                        r'Arbitraje < 1%': [],
                        r'Accesibles': [],
                        r'Arbitraje > 20%':  [],
                        r'max value - model {0}'.format(j): []
                        }
                df = pd.DataFrame(data)
                if update_table == True:
                        for file in files:
                                #CREATE TABLAS COMPARATIVAS
                                dicc[file] = pd.read_csv(ruta(['todos csv', str(j), file]))
                                maximo = dicc[file]['beneficio %'].tolist()
                                total = len(dicc[file].index)
                                maximos.append(maximo)
                                menor1 =  np.sum(dicc[file]['beneficio %'] < 1)/total
                                mayor20 =  np.sum(dicc[file]['beneficio %'] > 20)/total
                                centro = 1-(menor1 + mayor20)
                                df.loc[len(df.index)] = [file[:-4], dicc[file].shape[0], menor1, centro, mayor20,  max(maximo)]
                                path = ruta([f'{j}_tabla_comparativa.xlsx'])
                        df.to_excel(path, index= False)
                


                # # DIAGRAMA MAXIMO BENEFICIOS
                dicc =pd.read_excel(ruta([f'{j}_tabla_comparativa.xlsx']))
                if get_general_tab:
                        list_unic.append(dicc.set_index('days').iloc[:,np.arange(4)])
                        df_max_values['max value - model {0}'.format(j)] = (dicc.set_index('days')['max value - model {0}'.format(j)])
                val = {
                        1: '#8facff',
                        2: '#a171b4',
                        3: '#007fe2',
                        4: '#97e0c4',
                        5: '#000d14'
                        }
                dicc.plot(kind = 'line', x= 'days' , y = f'max value - model {j}', ax= plt.gca(), color = f'{val[j]}')
                plt.xlabel("Días", fontsize=16)
                plt.ylabel("Beneficio máximo", fontsize=16)
                
                if month_letter == True:
                        merged = []
                        for x in names:
                                x = x.split(".")
                                if   int(x[0]) == 3: merged.append("".join([x[1],'-', get_month(3).lower()]))
                                elif int(x[0]) == 4: merged.append("".join([x[1],'-', get_month(4).lower()]))
                                elif int(x[0]) == 5: merged.append("".join([x[1],'-', get_month(5).lower()]))
                                elif int(x[0]) == 6: merged.append("".join([x[1],'-', get_month(6).lower()]))
                        names = merged
                plt.xticks(np.arange(len(files)), names, rotation = 45, fontsize = 11, ha= 'right')
                plt.grid(linewidth = 0.35)
        if get_general_tab:
                list_unic = sum(list_unic)
                list_unic /=5
                list_unic['t'] = list_unic['t'].apply(lambda x: x*5)
                result = pd.concat([list_unic,df_max_values], axis= 1)
                for x in np.arange(5) +1:
                        result = result.rename({ f'max value - model {x}':f'modelo {x}'}, axis = 1)
                result.to_excel('resumen.xlsx')
        plt.show()
        return None

# def log_scale(total = 5):
#         for j in np.arange(total) + 1:
#                 #LEY DE POTENCIAS
#                 sns.distplot(dicc['03.22.22.csv']['beneficio %'], kde=False, color='#90c2e2',bins = len(maximo))
#                 plt.ylabel("Beneficios", labelpad=14)
#                 plt.xlabel("Frecuencia", labelpad=14)
#                 plt.title("Ley de potencias", fontsize=20, y=1.01)
#                 plt.show()

def comprobar_precios(dia, ruta = None, manual = False):
        dia += '.csv'
        capital = 1
        path = os.path.join(os.getcwd(),'arbitrage','exchangerate')
        matrix = pd.read_csv(os.path.join(path,dia), index_col = 'Unnamed: 0')
        #print(matrix)
        while manual == True:
                row = str(input('DE: ').upper())
                column =  str(input('A: ').upper())
                print(matrix.loc[row][column])
                print()
        if ruta:
                print(f'Capital inicial {capital}')
                for x in np.arange(len(ruta)-1):
                        DE = ruta[x]
                        A = ruta[x+1]
                        capital *= matrix.loc[DE][A]
                        print(f'{DE}/ {A} = {matrix.loc[DE][A]}')

def best_currency():
        dicc = defaultdict(dict)
        os.chdir(os.path.join(os.getcwd(),'RESULTS'))
        names = os.listdir(ruta(['todos csv','1']))
        #fundir = lambda lista: [maximos.append(item) for item in lista for item in item]
        for j in np.arange(5)+1:
                #CREATE TABLAS COMPARATIVAS
                buscar = re.compile(r'([A-Z]{3})')
                #[dicc[name[:-4]].append(x) for name in names for x in [re.findall(r'([A-Z]{3})',y) for y in pd.read_csv(ruta(['todos csv', str(j), name]))['rutas'].values]]
                for name in names:
                        dicc1 = pd.read_csv(ruta(['todos csv', str(j), name]), index_col= 'beneficio %')
                        dicc1['rutas'] = [x for x in [re.findall(r'([A-Z]{3})',y) for y in dicc1['rutas'].values]]
                        dicc1 =dicc1.drop(['Unnamed: 0'],axis = 1)
                        dicc[name[:-4]] = list(dicc1.to_dict().values())[0]
        return dicc
                         
def diagrama_burbujas(datos,nombre):
        lista = None
        for benef,ruta in datos[nombre].items():
                if benef > 20:
                        lista =[x for x in ruta if x != 'EUR']
        return lista



if __name__ == '__main__':
        comprobar_precios('08.17.22',manual= True)
        # libraries & dataset
        import seaborn as sns
        import matplotlib.pyplot as plt
        # set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above) 
        sns.set(style="darkgrid")
        df = sns.load_dataset("iris")

        sns.histplot(data=df, x="sepal_length", kde=True, color="skyblue", hue= 'petal_width') 
        plt.show()