
from cv2 import AKAZE
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import seaborn as sns
from arbitrage.meses import get_month
from collections import defaultdict
import re
from arbitrage import ArbitrageFinder as AF

ruta = lambda x: os.path.join(os.getcwd(),*x)

def randomize_color():
        lista = '0123456789ABCDEF'
        return "#" + "".join([lista[np.random.choice(len(lista))] for _ in range(6)])

def max_beneficio(total = 5, month_letter = False, update_table = False, get_general_tab= False, color= None) -> None:
        files = os.listdir(ruta(['RESULTS','todos csv','1']))
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
                                dicc[file] = pd.read_csv(ruta(['RESULTS','todos csv', str(j), file]))
                                maximo = dicc[file]['beneficio %'].tolist()
                                total = len(dicc[file].index)
                                maximos.append(maximo)
                                menor1 =  np.sum(dicc[file]['beneficio %'] < 1)/total
                                mayor20 =  np.sum(dicc[file]['beneficio %'] > 20)/total
                                centro = 1-(menor1 + mayor20)
                                df.loc[len(df.index)] = [file[:-4], dicc[file].shape[0], menor1, centro, mayor20,  max(maximo)]
                                path = ruta(['RESULTS',f'{j}_tabla_comparativa.xlsx'])
                        df.to_excel(path, index= False)
                
                # # DIAGRAMA MAXIMO BENEFICIOS
                dicc =pd.read_excel(ruta(['RESULTS',f'{j}_tabla_comparativa.xlsx']))
                if get_general_tab:
                        list_unic.append(dicc.set_index('days').iloc[:,np.arange(4)])
                        df_max_values['max value - model {0}'.format(j)] = (dicc.set_index('days')['max value - model {0}'.format(j)])
                if color != None:
                        a = np.arange(5) + 1
                        val = dict([(a[x],color[x]) for x in np.arange(len(a))])
                else: val = {
                        1: '#8facff',
                        2: '#a171b4',
                        3: '#007fe2',
                        4: '#97e0c4',
                        5: '#000d14'
                        }
                dicc.plot(kind = 'line', x= 'days' , y = f'max value - model {j}', ax= plt.gca(), color = f'{val[j]}')
                plt.xlabel("Días", fontsize=20)
                plt.ylabel("Beneficio máximo", fontsize=20)
                
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
        plt.close()
        return None

def log_scale():
        #for name in os.listdir(ruta(['todos csv','1'])):
        #LEY DE POTENCIAS
        df =all_currencies_together(get= 'df')
        #df = pd.read_csv(ruta(['RESULTS','todos csv','2','05.12.22.csv']))
        print(df)
        sns.set(style = 'whitegrid')
        sns.histplot(data = df, x = 'beneficio %',hue = 'model', log_scale= False, shrink= 0.9, kde= True) #hue = 'model',
        plt.ylabel("Conteo", labelpad=17)
        plt.xlabel("Beneficios %", labelpad=17)
        #plt.xticks(np.arange(df.shape(0)), datos_dia.keys(), rotation = 45, fontsize = 10, ha= 'right')
        plt.title("Histograma", fontsize=20, y=1.01)
        plt.show()

def diagrama_cajas(by= None):
        data = all_currencies_together(get = 'df')
        data['longitud'] = data['rutas'].apply(lambda x: len(x))
        a = (data[['rutas', 'beneficio %']].loc[data['longitud']== 8])
        a = a['rutas'].iloc[0]
        print(" -> ".join(a))
        fig, ax = plt.subplots()
        if by == 'beneficio':
                new = data.groupby('longitud')['beneficio %'].apply(list).to_dict()
                ax.boxplot(new.values())
                ax.set_xticklabels(new.keys())
        else:
                new = data.groupby('longitud').groups
                ax.boxplot(new.values())
                ax.set_xticklabels(new.keys())
        
        plt.xlabel("Longitud del camino") 
        plt.ylabel("Número de rutas") 
        plt.title("Correlacion beneficio - longitud del camino") 
        plt.tight_layout()
        plt.savefig('cajas_longitud_beneficio.pdf')
        plt.close()

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

def all_currencies_together(get = 'df') -> dict:
        ''' Devuelve un diccionario donde se almacena por dias otro diccionario con todas las agrupaciones
                {dia:{beneficio: ruta}}'''

       # temp_path = os.path.join(os.getcwd(),'RESULTS')
        names = os.listdir(ruta(['RESULTS','todos csv','1']))
        dicc = defaultdict(dict)
        df_dict = None
        #fundir = lambda lista: [maximos.append(item) for item in lista for item in item]
        df = []
        for j in np.arange(5)+1:
                #CREATE TABLAS COMPARATIVAS
                #buscar = re.compile(r'([A-Z]{3})')
                #[dicc[name[:-4]].append(x) for name in names for x in [re.findall(r'([A-Z]{3})',y) for y in pd.read_csv(ruta(['todos csv', str(j), name]))['rutas'].values]]
                concatenar = []
                for name in names:
                        dicc1 = pd.read_csv(ruta(['RESULTS','todos csv', str(j), name]))
                        n = dicc1.shape[0]
                        model_column = np.full(n,j)
                        dicc1['Unnamed: 0'] =dicc1['Unnamed: 0']+ np.full(n,names.index(name)*n+(j-1)*n*len(names))
                        dicc1 = dicc1.set_axis(dicc1['Unnamed: 0'])
                        dicc1['rutas'] = [x for x in [re.findall(r'([A-Z]{3})',y) for y in dicc1['rutas'].values]]
                        dicc1['model'] = model_column
                        dicc1['days'] = [name for _ in np.arange(n)]
                        dicc1 = dicc1.drop('Unnamed: 0', axis = 1)
                        #print(dicc1)
                        concatenar.append(dicc1)
                df.append(pd.concat(concatenar, axis= 0))
        df_dict = pd.concat(df, axis= 0)
        df_dict.loc[df_dict['beneficio %'] <=0,'beneficio %'] = 0.0001
        #df_dict.to_excel('ver.xlsx', index= False)
        if get == 'dict':
                #result = {day:{j:x for j,x in res} for day,res in df_dict.groupby(['days', 'beneficio %'])['rutas']}
                result = {}
                for day, res in df_dict.groupby('days'):
                        #result[day].append(dict([(res.values.tolist()[:2][n:n+2]) for n in np.arange(0,len(res.values.tolist()[:2]),2)]))
                        result[day[:-4]] = dict([(x[:2]) for x in (res.values.tolist())])
                #print(result)
                return result
        elif get == 'df': return df_dict
                         
def conteo_divisas(beneficio) -> dict:
        '''
        Devuelve un dicc de todas las monedas con el numero de repeticiones que estas tienen segun
        el beneficio que le indiquemos
        params. beneficio = int()
        return. dict(all_currencies)
        '''
        def count_num_currencies(datos):
                lista = []
                for benef,ruta in datos.items():       
                        [lista.append(x) if benef > beneficio else None for x in ruta if x != 'EUR']
                return lista
                
        list_monedas = AF().monedas
        names = os.listdir(ruta(['RESULTS','todos csv','1']))
        data = all_currencies_together(get = 'dict')
        lista = []
        num = 0
        for name in names:
                dato = count_num_currencies(data[name[:-4]])
                num += len(dato)
                if dato != None: [lista.append(x) for x in dato]
        counter = {i:lista.count(i)/num*100 for i in lista}
        add = list(set(list_monedas).difference(set(counter)))
        for x in add:
                if x != "EUR": counter[x] = 0
        counter = {k:v for k,v  in sorted(counter.items(), key= lambda x: x[1], reverse= True)}
        counter = dict(list(counter.items()))
        return counter

def pie_chart(beneficio = 20, merged_below = None, color = None) -> None:
        counter = conteo_divisas(beneficio)
        if color == None: colores = [randomize_color() for _ in range(len(counter))]
        else: colores = color

        if merged_below  != None:
                rest ={k:v for k, v in counter.items() if v <= merged_below}
                for k in rest:
                        del counter[k]
                values = rest.values()
                counter[f'< {max(values):.02f}% ({len(values)} divisas)'] = sum(values)
        plt.pie(counter.values(), labels=counter.keys(), autopct= '%1.1f%%', colors=colores)
        plt.axis("equal")
        plt.title(f'Porc.de aparicion de monedas mayor a un {beneficio} % de beneficio\n')
        #plt.show()
        name = str(beneficio)+".pdf"
        plt.savefig(ruta([name]))
        plt.close()
        return 0
        
def longitud_caminos():
        data = all_currencies_together(get = 'df')
        data['longitud'] = data['rutas'].apply(lambda x: len(x)-1)
        print(data[['rutas', 'beneficio %']].loc[data['longitud']== 8])
        sns.scatterplot(y='beneficio %', 
                        x='longitud', 
                        alpha=0.3, 
                        data=data) 
        
        plt.xlabel("Longitud del camino") 
        plt.ylabel("Beneficio (%)") 
        plt.title("Correlacion beneficio - longitud del camino") 
        plt.tight_layout()
        plt.grid(axis = 'y',linewidth= 0.3)
        #plt.show()
        plt.savefig('correlacion_benef_long.pdf')
        plt.close()



if __name__ == '__main__':
        c = ['#f5e7e4','#ecd2d8','#d2b1c5','#b59eb7','#958e9e']

        #max_beneficio(5, get_general_tab= False, update_table= False, color = None)
        #comprobar_precios('05.19.22',['EUR', 'ZWL', 'BYN', 'EUR'], manual= False)
        #pie_chart(beneficio = 1, merged_below=1,color = c)
        #pie_chart(beneficio = 5, merged_below=2, color = c)
        pie_chart(beneficio = 20, merged_below=None, color = c)
        # diagrama_cajas()
        # longitud_caminos()