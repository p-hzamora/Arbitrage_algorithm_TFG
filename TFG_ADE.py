from arbitrage import ArbitrageFinder as AF
from time import time
import os

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

def prueba2():
    to = time()
    arbitrage = AF(
                    tipo= 'xlsx',
                    currency= 'USD',
                    filename= '3_divisas.xlsx',
                    log = True,
                    rnd= True
                    )
    arbitrage.print_data()

    print("Grafo de sucesores")
    arbitrage.digraph.print_graph()
    arbitrage.simulated_annealing(14.28)
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
        currency= 'EUR',
        tipo = 'csv',
        rnd= True,
        starting_amount= 1000)
    #print(arbitrage.url())
    a = arbitrage.simulated_annealing_random(profit)
    #print(a)
    final = time()-to
    print(f"\n[Finalizado TOTAL en {final:.02f} s]\n\n")

def SA(pesos= False, nodos = False, imprimir= False):
    a = AF(
        currency= 'EUR',
        rnd= True,
        starting_amount= 1000)
    if pesos:
        a.intervalo = intervalo =  a.digraph.weights
    elif nodos:
        a.intervalo = intervalo =  a.digraph.scraper.monedas
    else:
        intervalo = (-3,5)
    
    eje_x, c, states, costs = a.simulated_annealing(
        intervalo,
        maxsteps=1_000,
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
    
def update_SA(pesos= False, nodos = False, imprimir= False):
    a =AF(currency='EUR')
    if pesos:
        intervalo =  a.digraph.weights
    elif nodos:
        intervalo =  a.digraph.scraper.monedas
    else:
        intervalo = (-3,5)
        
    eje_x, c, states, costs = a.update_SA(
        intervalo,
        maxsteps=1_000,
        debug= False,
        c_nodes = nodos,
        c_weight= pesos,
        )
    print(f"Valor en X: {eje_x}")
    print(f"Estado: {c}")
    if imprimir and all([nodos, pesos])== False:
        a.see_annealing(states, costs)
    else: print(a.profit_and_path[a._SA])
    
        
if __name__ == "__main__":
    pruebaAPI()
    #prueba_annealing(3)
    #SA(pesos= True, imprimir = True)    
    
    update_SA(pesos = True, imprimir = True)
    os.system('pause')
