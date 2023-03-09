#USB

from .glob import Glob
from arbitrage.currencyDigraph import CurrencyDigraph
from arbitrage.parameter import Parameter
from arbitrage.utils import printcol
from arbitrage.keyGenerator import KeyGenerator	#Aunque no se use, se pone para poder acceder a los metodos de la clase por @classmethod
from arbitrage.errors import *
import numpy as np
import time

from arbitrage.scraper import Scraper as sp

__author__  = " Pablo Hernandez  <p.hzamora@alumnos.upm.es>"
__status__  = "Arbitrage finder"
__version__ = "2.0"




class ArbitrageFinder(Parameter):
	OPTIMIZE_PROFIT = 0
	OPTIMIZE_PATH = []
	def mide_tiempo(funcion):
		def funcion_medida(*args, **kargs):
			inicio = time.time()
			c = funcion(*args, **kargs)
			final = time.time() - inicio
			print(f"[Finalizado en {final:.02f} s]")
			return c
		return funcion_medida
	  
	def __init__(self, tipo = 'csv', filename = 'exchangerate.csv', password = None, \
     			filtro = None, rnd = False, starting_amount = 1, currency = 'USD', log = True):
		super().__init__( tipo, filename, password, filtro, rnd, log)
		self._currency = currency
		self._starting_amount = starting_amount

		self._profit = [-np.inf]
		self._profit_and_path = {}
		self.__e = np.exp(1)
		self._digraph = CurrencyDigraph(self._tipo, self._filename, self._password, self._filtro, self._currency, rnd = self._rnd, log = self._log)
		self._src = self._digraph.scraper._strs[self._currency] 	

		self._Ppesos = self._digraph.weights 
		self._rutaBF = None
		self._pesoBF = None
		self._interval = any
		self._maxsteps = any
		self._SA = None

	@property
	def monedas(self):
		return self._digraph.scraper._strs

	@property	
	def intervalo(self):
		return self._interval
	@intervalo.setter
	def intervalo(self, a):
		self._interval = a
	@property
	def digraph(self):
		return self._digraph

	@property
	def profit_and_path(self):
		return self._profit_and_path

	def url(self):
		if self._password == None:
			return None
		return f'https://v6.exchangerate-api.com/v6/{self._password}/latest/USD'
	
	def print_data(self):
		return self._digraph.scraper.print_data()

	def get_arbitraje(self):
		"""
		Get the arbitrage cycle.
		
		:param amount: starting amount
		:param cycle: found cycle
		:param W: weights hashmap
		:param keys: hashmap of keys from ID to currency code
		:returns: void
		"""
		cycle = self._digraph.find_cycle(self._src)
		result_amount = self._starting_amount
		trade_sequence = []
		pesos_rutas = 0
		for i in range(len(cycle)):
			DE = self._digraph.scraper._keys[cycle[i]]
			A = self._digraph.scraper._keys[cycle[(i+1)%len(cycle)]]
			pesos_rutas += self._digraph.weights[(DE,A)]
			trade_sequence.append(DE)
		result_amount *= self.__e**-pesos_rutas
		profit_percent = (self.__e**-pesos_rutas-1) *100
  
		trade_sequence.insert(0,self._currency)
		self._profit.append(profit_percent)
		self._profit_and_path[profit_percent]= trade_sequence
		self._digraph.predecesora ={}
		if ArbitrageFinder.OPTIMIZE_PROFIT < profit_percent: 
			ArbitrageFinder.OPTIMIZE_PROFIT = profit_percent
			ArbitrageFinder.OPTIMIZE_PATH = trade_sequence
		return profit_percent, trade_sequence	#Se quiere minimizar la funcion, por eso debemos extraer el primer parametro, el segundo sirve como clave a la hora de buscar la ruta en el total

	def print_arbitraje(self):
		"""
		A helper method for printing the arbitrage cycle. Shows how much can 
		be made relative to the starting amount. Prints details of arbitrage
		opportunity.
  		"""
		print()
		print('Camino para arbitraje')
		print('='*22,'\n')
		print(f'Moneda base:', end= " ")
		printcol(f'{self._currency}','AMARILLO_CLARO')
		print()
		orig = result_amount = self._starting_amount
		profit_percent = self._profit[-1]
		result_amount *= (1+ profit_percent/100)
		printcol(f' -> '.join(self._profit_and_path[self._profit[-1]]), 'VERDE_CLARO')
		print("Capital inicial: {:.03f}  |  Capital final: {:.03f}  |  % de beneficio: {:.05f} %)".format(orig, result_amount, profit_percent))
		print("Beneficio: {:.04f} {}".format(result_amount-orig,self._currency))
		return 0

	def print_cycle(self):
		print("Shortest path:")
		printcol("{}".format(" -> ".join(self._rutaBF)), 'VERDE_CLARO')
		print(f'Weight of the path: {self._pesoBF}')
		print()

	def bellman_ford_no_negative_cycles(self, final, inicio = None):
		"""
		Algoritmo de Bellman-Ford clasico
		"""
		if inicio == None:
			inicio = self._currency
		lista= []
		for _ in range(len(self._digraph.graph)-1):
			for w in self._digraph.weights:
				# w is a tuple in the form of (u, v)
				u, v = w
				temp = np.inf
				if self._digraph._distances[u] != np.inf and self._digraph.weights[w] != '-':
					temp = self._digraph._distances[u] + self._digraph.weights[w] # distance(u) + weight(u, v)
					if  self._digraph._distances[v] > temp: # if shorter path found
						self._digraph._distances[v] = temp
						self._digraph.predecesora[v] = u
						if v == self._currency: # negative path back to source found. Terminate
							raise negativeCycleDetected
		lista.append(final)
		i = final
		while i in self._digraph.predecesora.keys():
			temp = self._digraph.predecesora[i]
			lista.append(temp)
			i =temp
		lista = lista[::-1]
		self._rutaBF = lista[lista.index(inicio):lista.index(final)+1]
		self._pesoBF = self._digraph._distances[final]
		return self._rutaBF, self._pesoBF
	
	def bellman_ford(self):
		"""
		Algoritmo de Bellman-Ford para detectar ciclos negativos.
		
		:param src: starting currency
		:param starting_amount: starting amount in currency
		:returns: void
		"""
		if not sp.Pmonedas:
			sp.Pmonedas = self._digraph.scraper.monedas
		cx = 0
		max = len(self._digraph.graph)-1
		# self._digraph.weights = dict(sorted(self._digraph.weights.items(),key = lambda x: x[-1], reverse= False))
		for _ in range(max):
			cx +=1
			#print(f"\nBucle {cx} (max: {max})")
			c = 0
			for w in self._digraph.weights:	
				c +=1
				#print(f"\r{c}", end= "")
				# w is a tuple in the form of (u, v)
				u, v = w
				temp = np.inf
				if self._digraph._distances[u] != np.inf and self._digraph.weights[w] != '-' :
					temp = self._digraph._distances[u] + self._digraph.weights[w] # distance(u) + weight(u, v)
					if  self._digraph._distances[v] > temp: # if shorter path found
						self._digraph._distances[v] = temp
						self._digraph.predecesora[v] = u
						if v == self._currency: # negative path back to source found. Terminate
							#print('') #Lo usamos para que el printa de arriba no de errores de impresion
							return *self.get_arbitraje(), c
		# negative cycle detection
		for w in self._digraph.weights:
			u, v = w
			if self._digraph.weights[w] != '-':
				temp = self._digraph._distances[u] + self._digraph.weights[w]
				if v == self._src: # limit to only cycles including src currency
					if temp < self._digraph._distances[v]:
						return self.get_arbitraje()
		return 'NO HAY ARBITRAJE'	# Si la funcion llega a este punto no hay arbitraje, pues se deberia haber salido antes
  
	@mide_tiempo
	def RANDOM(self, optimo= 1):
		'''
  		Algoritmo para obtener la ruta optima de arbitraje
    	'''
		raise Exception('Funcion no actualizada')
		to = time.time()
		if self._rnd == False: raise CantExecuteSimulatedAnnealing
		# while self._profit[-1] < optimo:
		for _ in range(optimo):
			self.bellman_ford()
			self._digraph.scraper.set_rnd_monedas()
			self._digraph = CurrencyDigraph(self._tipo, self._filename, self._password, self._filtro, self._currency, rnd = self._rnd, log= self._log)
		#self.print_arbitraje()
		return self._profit_and_path


	def test_arbitrage(self, accuracy= 0.0001):
		return self._digraph.scraper.test_arbitrage(accuracy = accuracy)

	def __reset(self):
		self._digraph.scraper._rates = {}
		self._digraph.predecesora = {}
		self._digraph._distances = {vertex: np.inf for vertex in self._digraph.graph}
		self._digraph.set_source(self._digraph._src)

	def __sort_dict(self, dicc, by, repeat = False) -> dict:
		"""
		Funcion para mover una parte concreta del diccionario a los primeros valores de este.
		Uso destino a dicc con claves en formato tupla
			dicc = {(0, 5): 'A', (1, 6): 'B', (2, 7): 'C', (3, 8): 'D', (4, 9): 'E', (5, 10)} 
			sort(dicc, 2)
		"""
		if not repeat and Glob.sort_dict > 0: return self._digraph.weights
		Glob.sort_dict = 1
		n = self._digraph.scraper._key
		if len(dicc) < len(self._digraph.scraper.monedas): raise Exception('diccionario menor al numero de monedas')
		pivot = list(map(lambda x: x[0],dicc.keys())).index(by)
		if pivot == 0: return dicc
		elif pivot + n != len(self._digraph.weights):    
			return dict([*list(dicc.items())[pivot:pivot+ n],*list(dicc.items())[:pivot], *list(dicc.items())[pivot + n:]])
		else:
			return dict([*list(dicc.items())[pivot:pivot+ n],*list(dicc.items())[:pivot]])

	def __set_rnd_pesos(self,pivot):
		'''
		Realizar un unico intercambio entre 2 valores del diccionario
		Antes de hacer el swap, ordenamos una vez
		'''
		self._digraph.weights = self.__sort_dict(self._digraph.weights, self._digraph._src, repeat = False)
		
		# lista = np.arange(0,len(self._digraph.weights))
		# rdm = (np.random.choice(lista,2,replace= False))
		# fin = np.random.randint(pivot,len(lista))
		

		ini = np.random.randint(0,pivot)
		fin = list(self._digraph.weights.values()).index(min(list(self._digraph.weights.values())[pivot:]))
		rdm = (ini,fin)
		#print(rdm)
		#realizamos swap
		lista_dict = list(self._digraph.weights.items())
		temp = lista_dict[rdm[1]]
		lista_dict[rdm[1]] = lista_dict[rdm[0]]
		lista_dict[rdm[0]] = temp
		self._digraph.weights =dict(lista_dict) 

		return rdm

	@staticmethod
	def function(x):
		""" Funcion a minimizar."""
		return 50 + np.exp(x) + np.exp(-x/2) * np.cos(2*np.pi*x) + np.cos(4* x**2)

	def see_annealing(self, states, costs):
		import matplotlib.pyplot as plt  # to plot

		plt.figure(figsize=(19,8))
		plt.suptitle("Evolucion en eje X y coste de la funcion")
  
		plt.subplot(221)
		plt.title("Estados")
		plt.ylabel('Eje x')
		plt.plot(states, '#ff5e5e')
		plt.grid()
  
		plt.subplot(223)
		plt.title("Costes")
		plt.ylabel('Valores')
		plt.plot(costs, '#90c2e2')
		plt.grid()
  
		plt.subplot(122)
		plt.title("Funcion a minimizar f(x)")
		plt.ylabel('Eje y')
		plt.xlabel('Eje x')
		x = np.linspace(self._interval[0],self._interval[1], self._maxsteps)
		plt.plot(x, self.function(x), '#90c2e2')
		plt.grid()
		plt.show()

	@mide_tiempo
	def simulated_annealing_random(self, optimo= 1):
		'''
  		Algoritmo para obtener la ruta optima de arbitraje
    	'''
		result = {}
		while self._profit[-1] < optimo:
		#while len(result) < optimo:
			cost, ruta, _ = self.bellman_ford() #[0] valor invertido logaritmico [1] ruta para llegar a ese valor
			result[cost] =ruta
			self.__reset()
			self._digraph.scraper.set_rnd_monedas()
			#actualizamos la variable que guarda los pesos
			self._Ppesos = self._digraph.weights = self._digraph.scraper._rates
			#self.print_arbitraje()
		return result
	@mide_tiempo
	def simulated_annealing(self, interval,  maxsteps=1000, debug=False,c_nodes = False, c_weight = False):
		"""
		simulated annealing optimization algorithm that takes a cost function
		and tries to minimize it by looking for solutions from the given domain
		requirements: is to define the costf which is needed to be minimized for
		error functions and domain which is a random solution to begin with
		"""
		self._interval = interval
		self._maxsteps = maxsteps

		def clip(x):
			""" Forzar a x a estar dentro del intervalo"""
			a, b = self._interval
			return max(min(x, b), a)
		
		def random_start():
			"""Obtener valor random del intervalo."""
			a, b = self._interval 
			return a + (b - a) * np.random.random_sample()	
		
		def cost_function(x):
			""" Cost of x = f(x)."""
			return self.function(x)
		
		def random_vecino(x= None, fraction= 1):
			"""Move a little bit x, from the left or the right."""
			lista = np.arange(0,self._interval[1])
			def nodos():
				rdm = (np.random.choice(lista,2,replace= False))
				pos_1 = list(lista).index(rdm[0])
				pos_2 = list(lista).index(rdm[1])
				#realizamos swap
				monedas = list(lista)
				temp = monedas[pos_2]
				monedas[pos_2] = monedas[pos_1]
				monedas[pos_1] = temp
				self._digraph.scraper.monedas = monedas
				return np.random.sample()*len(self._digraph.scraper.monedas)

			def pesos():
				rdm = (np.random.choice(lista,2,replace= False))
				pos_1 = list(lista).index(rdm[0])
				pos_2 = list(lista).index(rdm[1])
				#realizamos swap
				lista_dict = list(self.digraph.weights.items())
				temp = lista_dict[pos_2]
				lista_dict[pos_2] = lista_dict[pos_1]
				lista_dict[pos_1] = temp
				self._digraph.weights = dict(lista_dict)
				return np.random.sample()*len(self._digraph.weights)

			amplitude = (max(self._interval) - min(self._interval)) * fraction / 10
			if x!= None:
				delta = (-amplitude/2.) + amplitude * np.random.random_sample()
				return clip(x + delta)
			elif c_nodes:
				nodos()
			elif c_weight:
				pesos()

		def acceptance_probability(cost, new_cost, temperature):
			if new_cost < cost:
				# print("    - Acceptance probabilty = 1 as new_cost = {} < cost = {}...".format(new_cost, cost))
				#accept = np.exp(1)**-abs(cost-new_cost)/temperature
				#return accept
				return 1
			else:
				p = np.exp(- (new_cost - cost) / temperature)
				# print("    - Acceptance probabilty = {:.3g}...".format(p))
				return p
			
		def temperature(fraction):
			""" Example of temperature dicreasing as the process goes on."""
			return max(0.01, min(1, 1 - fraction))
    
    #______________________________________________________________________________________________________________________________________________________
		state = 4 #random_start()
		# state = -3 # maple para obtener funciones mathematica
		cost = cost_function(state)
		states, costs = [state], [cost]
		for step in range(self._maxsteps):
			fraction = step / float(self._maxsteps)
			T = temperature(fraction)
			new_state = random_vecino(state, fraction)
			new_cost = cost_function(new_state)
			if debug: print(f"Step #{step}/{self._maxsteps} : T = {T}, state = {state}, cost = {cost}, new_state = {new_state}, new_cost = {new_cost}")
			if acceptance_probability(cost, new_cost, T) > np.random.random():
				state, cost = new_state, new_cost
				states.append(state)
				costs.append(cost)
		return state, cost_function(state), states, costs

	@mide_tiempo
	def simulated_annealing_merged(self, maxsteps=1000, debug=False,c_nodes = False, c_weights = False):
		'''
  		Algoritmo para obtener la ruta optima de arbitraje
    	'''
		self._maxsteps = maxsteps 

		def acceptance_probability(cost, new_cost, temperature):
			if new_cost < cost:
				# print("    - Acceptance probabilty = 1 as new_cost = {} < cost = {}...".format(new_cost, cost))
				#accept = np.exp(1)**-abs(cost-new_cost)/temperature
				#return accept
				return 1
			else:
				p = np.exp(- (new_cost - cost) / temperature)
				# print("    - Acceptance probabilty = {:.3g}...".format(p))
				return p
			
		def temperature(fraction):
			""" Example of temperature dicreasing as the process goes on."""
			return max(0.01, min(1, 1 - fraction))

		def random_vecino():
			if c_weights: self.__set_rnd_pesos(max_loop)
			elif c_nodes:
				self._digraph.scraper.set_rnd_monedas()
				self._digraph.weights = self._digraph.scraper._rates 
			return 0

		def updated_state(forward = True):
			if forward: return sp.Nmonedas

			if c_weights: return self._digraph.weights
			elif c_nodes: return sp.Pmonedas

		# _____________________________________________________________________________________________________________________________
		contador = 1
		#if self._rnd == False: raise CantExecuteSimulatedAnnealing
		cost, _, max_loop = self.bellman_ford() #[0] valor invertido logaritmico [1] ruta para llegar a ese valor
		self.__reset()
		state = updated_state()
		states,costs = [state], [cost]
		
		for step in range(self._maxsteps):
			fraction = step / float(self._maxsteps)
			T = temperature(fraction)
			random_vecino()
			new_cost,ruta, max_loop = self.bellman_ford()
			self.__reset()
			if debug: print(f"Step #{step}/{self._maxsteps} : T = {T}, state = {state}, cost = {cost}, new_state = {sp.Nmonedas}, new_cost = {new_cost}")
			if acceptance_probability(cost, new_cost, T) > np.random.random():
				#Si aceptamos actualizamos 
				state, cost = updated_state(forward = True), new_cost
				states.append(state)
				costs.append(cost)
				print(cost)
			else: #para restaurar la red de pesos 
				self._digraph.weights = self._Ppesos 

			if len(set(costs)) > contador:
				contador +=1
				#self.print_arbitraje()
				# self._profit_and_path[max(self._profit_and_path)] Para comprobar cual de todo el diccionario es el punto mas optimo
		return self._profit_and_path[list(self._profit_and_path)[-1]]