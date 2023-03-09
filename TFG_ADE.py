import pandas as pd
from arbitrage import ArbitrageFinder as AF
from time import time 

import os
import concurrent.futures
from collections import defaultdict
import numpy as np
import datetime

def prueba_sin_bucles():
    to = time()
    arbitrage = AF(
                    tipo= 'xlsx',
                    currency= 'A',
                    filename= 'ejemplo_hoja.xlsx',
                    log = False
                    )
    arbitrage.print_data()

    print("Grafo de sucesores")
    arbitrage.digraph.print_graph()

    arbitrage.bellman_ford_no_negative_cycles(final= 'D')

    arbitrage.print_cycle()
    print('Distancias de cada nodo')
    arbitrage.digraph.print_distances()
    final = time()-to
    print(f"\n[TOTAL en {final:.02f} s]\n\n")
    os.system('pause')

def prueba2(step, nodos = False, pesos = False):
    to = time()
    arbitrage = AF(
                    starting_amount= 1000,
                    tipo= 'xlsx',
                    currency= 'USD',
                    filename= '3_divisas.xlsx',
                    log = True,
                    rnd= True
                    )
    arbitrage.print_data()

    print("Grafo de sucesores")
    arbitrage.digraph.print_graph()
    ruta = arbitrage.simulated_annealing_merged(maxsteps= step, c_nodes= nodos, c_weights= pesos)
    print(ruta)
    arbitrage.print_arbitraje()
    print('Distancias de cada nodo')
    arbitrage.digraph.print_distances()
    final = time()-to
    print(f"\n[TOTAL en {final:.02f} s]\n\n")
    os.system('pause')

def pruebaAPI():
    to = time()
    arbitrage = AF(currency= 'EUR', tipo = 'api', rnd= True, starting_amount= 10000)
    #print(arbitrage.url())
    arbitrage.bellman_ford()
    arbitrage.print_arbitraje()
    final = time()-to
    print(f"\n[TOTAL en {final:.02f} s]\n\n")
    #_, _, a = arbitrage.test_arbitrage()

def prueba_annealing(profit):
    to = time()
    arbitrage = AF(
            starting_amount= 1000,
            currency= 'EUR',
            rnd = True
            )
    #print(arbitrage.url())
    a = arbitrage.RANDOM(profit)
    arbitrage.print_arbitraje()
    #print(a)
    final = time()-to
    print(f"\n[Finalizado TOTAL en {final:.02f} s]\n\n")

def SA(maxsteps, pesos= False, nodos = False, imprimir= False):
    a = AF(
        currency= 'EUR',
        tipo = 'csv',
        rnd= True,
        starting_amount= 1000)
    if pesos:
        a.intervalo = intervalo =  (0, len(a.digraph.weights))
    elif nodos:
        a.intervalo = intervalo =  (0, len(a.digraph.scraper.monedas))
    else:
        intervalo = (-2,4)
    
    eje_x, c, states, costs = a.simulated_annealing(
        intervalo,
        maxsteps= maxsteps,
        debug= False,
        c_nodes = nodos,
        c_weight= pesos,
        )
    print(f"Valor en X: {eje_x}")
    print(f"Coste: {c}")
    if imprimir and all([nodos, pesos])== False: a.see_annealing(states, costs)
    else: print(a.profit_and_path[a._SA])
    
def prueba_linspace():
    import numpy as np
    import matplotlib.pyplot as plt
    
    a= np.linspace(0, 100, 10)    
    plt.plot(a, a**2)
    plt.show()
    
def SA_merged(step, nodos = False, pesos = False):
    a =AF(currency='EUR')
    ruta = a.simulated_annealing_merged(maxsteps= step, c_nodes= nodos, c_weights= pesos)
    print(ruta)
        










def FINAL(nombre, max_iter=1):
    arbitrage = AF(
            starting_amount= 1000,
            filename= nombre,
            currency= 'EUR',
            rnd= True
            )
    #print(arbitrage.url())
    a = arbitrage.simulated_annealing_random(max_iter)

    return (nombre,a)

# def contar(extension, dir_data):
#     ruta = lambda x: os.path.join(os.getcwd(),'RESULTS',*x)
#     data_path = ruta(dir_data)

#     data = [x for x in os.listdir(data_path) if x.endswith('.'+ extension)]
#     for file in data:
#         if extension == 'csv': df = pd.read_csv(os.sep.join([data_path,file]))
#         elif extension == 'xlsx': df = pd.read_excel(os.sep.join([data_path,file]))
#         rows = df.shape[0]
#         return abs(2000-rows)

def contar(dir_data):
    ruta = lambda x: os.path.join(os.getcwd(),'RESULTS',*x)
    data_path = ruta(dir_data)
    df = pd.read_csv(data_path)
    rows = df.shape[0]
    return abs(2000-rows)
      

def exposicion(optimo,**kargs): 
    if kargs == {}:
        arbitrage = AF()
    else:
        arbitrage = AF(
                starting_amount = kargs['starting_amount'],
                currency = kargs['currency'],
                rnd = kargs['rnd']
                )           
    a = arbitrage.simulated_annealing_random(optimo)
    b = arbitrage.print_arbitraje()
    print(a)




if __name__ == "__main__":
    #pruebaAPI()
    #prueba2(1000, pesos= True)
    #prueba_annealing(5)
    SA(imprimir = True, maxsteps=500_000)    
    #SA_merged(1000, nodos= True)
    exposicion( optimo =5,
                starting_amount= 1000,
                currency= 'EUR',
                rnd= True
                )

    # ruta = os.path.join(os.getcwd(),'arbitrage','exchangerate')
    # lista = [x for x in os.listdir(ruta) if x.endswith('.csv')]

    # print(datetime.datetime.now())

    # save = np.arange(0,70,10)

    # vuelta = 2
    # print("Carpeta {0}".format(vuelta))
    # for i in range(len(save)-1):
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         futures = []
    #         for nombre in lista[save[i]:save[i+1]]: 
    #             row = 1000
    #             print(f'{nombre} | rows: {row}')
    #             futures.append(executor.submit(FINAL, nombre = nombre, max_iter = row))
    #     #lista de cada extraccion sacada de la API
    #     extraccion = dict([future.result() for future in concurrent.futures.as_completed(futures)])

    #     data = defaultdict(list)
    #     ruta = lambda x: os.path.join(os.getcwd(),'RESULTS', *x)
        
    #     for files in extraccion:
    #         data['beneficio %'] = extraccion[files].keys()
    #         data['rutas'] = extraccion[files].values()
    #         df = pd.DataFrame(data)
    #         name = "".join(files.split('.csv')) + '.xlsx'
    #         df.to_excel(ruta(['todos excel',str(vuelta), name]), sheet_name= files, index= False)
