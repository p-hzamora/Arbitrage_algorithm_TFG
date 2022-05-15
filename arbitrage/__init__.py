from arbitrage.divisasDigraph import CurrencyDigraph
from arbitrage.datatypes import Parameter
from arbitrage.utils import printcol
from arbitrage.keyGenerator import KeyGenerator	#Aunque no se use, se pone para poder acceder a los metodos de la clase por @classmethod
from arbitrage.errors import *
import numpy as np
import time

__author__  = " Pablo Hernandez  <p.hzamora@alumnos.upm.es>"
__status__  = "Arbitraje"
__version__ = "0.1.0.0"




class ArbitrageFinder(Parameter):
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
  
		self._rutaBF = None
		self._pesoBF = None
		self._interval = any
		self._maxsteps = any
		self._cal_by_nodes = None
		self._cal_by_weight = None
		self._SA = None

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
		print(trade_sequence,profit_percent)
		return pesos_rutas, profit_percent	#Se quiere minimizar la funcion, por eso debemos extraer el primer parametro, el segundo sirve como clave a la hora de buscar la ruta en el total

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
		printcol(' -> '.join(self._profit_and_path[self._profit[-1]]), 'VERDE_CLARO')
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
  
	def bellman_ford(self,pesos):
		"""
		Algoritmo de Bellman-Ford para detectar ciclos negativos.
		
		:param src: starting currency
		:param starting_amount: starting amount in currency
		:returns: void
		"""
		self._digraph.weights = pesos
		for _ in range(len(self._digraph.graph)-1):
			for w in self._digraph.weights:
				u, v = w
				temp = np.inf
				if self._digraph._distances[u] != np.inf and self._digraph.weights[w] != '-' :
					temp = self._digraph._distances[u] + self._digraph.weights[w] # distance(u) + weight(u, v)
					if  self._digraph._distances[v] > temp: # if shorter path found
						self._digraph._distances[v] = temp
						self._digraph.predecesora[v] = u
						if v == self._currency: # negative path back to source found. Terminate
							return self.get_arbitraje()
		# negative cycle detection
		for w in self._digraph.weights:
			u, v = w
			if self._digraph.weights[w] != '-':
				temp = self._digraph._distances[u] + self._digraph.weights[w]
				if v == self._src: # limit to only cycles including src currency
					if temp < self._digraph._distances[v]:
						return self.get_arbitraje()
		raise noArbitrage	# Si la funcion llega a este punto no hay arbitraje, pues se deberia haber salido antes
  
	def test_arbitrage(self, accuracy= 0.0001):
		return self._digraph.scraper.test_arbitrage(accuracy = accuracy)

	@mide_tiempo
	def simulated_annealing_random(self, optimo= 1):
		'''
  		Algoritmo para obtener la ruta optima de arbitraje
    	'''
		if self._rnd == False: raise CantExecuteSimulatedAnnealing
		while self._profit[-1] < optimo:
			self.bellman_ford()
			self._digraph.scraper.set_rnd_monedas()
			self._digraph = CurrencyDigraph(self._tipo, self._filename, self._password, self._filtro, self._currency, rnd = self._rnd, log= self._log)
			self.print_arbitraje()
		return self._profit_and_path[list(self._profit_and_path)[-1]]

	def see_annealing(self, states, costs):
		import matplotlib.pyplot as plt  # to plot

		plt.figure(figsize=(19,8))
		plt.suptitle("Evolucion en eje X y coste de la funcion")
  
		plt.subplot(221)
		plt.title("Estados")
		plt.ylabel('Eje x')
		plt.plot(states, 'r')
		plt.grid()
  
		plt.subplot(122)
		plt.title("Costes")
		plt.ylabel('Valores')
		plt.plot(costs, 'b')
		plt.grid()
  
		plt.subplot(223)
		plt.title("Funcion a minimizar")
		plt.ylabel('Eje y')
		plt.xlabel('Eje x')
		x = np.linspace(self._interval[0],self._interval[1], self._maxsteps)
		plt.plot(x, self.f(x))
		plt.grid()
  
		plt.show()

	def f(self,x):
		""" Funcion a minimizar."""
		if  any((self._cal_by_nodes,self._cal_by_weight)) == False:
			return 5*x**4 - 10*x**2 + 5*x** 3 -x
		else: 
			separate = self.bellman_ford(x)
			self._SA = separate[1]
			return separate[0]

	@mide_tiempo
	def simulated_annealing(self, interval,  maxsteps=1000, debug=False,c_nodes = False, c_weight = False):
		"""
		simulated annealing optimization algorithm that takes a cost function
		and tries to minimize it by looking for solutions from the given domain
		requirements: is to define the costf which is needed to be minimized for
		error functions and domain which is a random solution to begin with
		"""
		self._cal_by_nodes = c_nodes
		self._cal_by_weight = c_weight
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
			return self.f(x)
		
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
		state = random_start()
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
	def update_SA(self, interval,  maxsteps=1000, debug=False,c_nodes = False, c_weight = False):
		"""
		simulated annealing optimization algorithm that takes a cost function
		and tries to minimize it by looking for solutions from the given domain
		requirements: is to define the costf which is needed to be minimized for
		error functions and domain which is a random solution to begin with
		"""
		self._cal_by_nodes = c_nodes
		self._cal_by_weight = c_weight
		self._maxsteps = maxsteps
  
		def swap(range):
			'''
			Realizar un unico intercambio entre 2 valores del diccionario
			'''
			if isinstance(range,dict):
				lista = np.arange(0,len(range))
				rdm = (np.random.choice(lista,2,replace= False))
				#realizamos swap
				lista_dict = list(range.items())
				temp = lista_dict[rdm[1]]
				lista_dict[rdm[1]] = lista_dict[rdm[0]]
				lista_dict[rdm[0]] = temp
				range =dict(lista_dict)
			elif any((isinstance(range,list),isinstance(range,set))):
				range = list(range)
				lista = np.arange(0,len(range))
				rdm = (np.random.choice(lista,2,replace= False))
				#realizamos swap
				#rdm = (0,1)
				temp = range[rdm[1]]
				range[rdm[1]] = range[rdm[0]]
				range[rdm[0]] = temp
			return range
		def clip(x):
			""" Forzar a x a estar dentro del intervalo"""
			a, b = self._interval
			return max(min(x, b), a)
		def random_start(x):
			"""Obtener valor random del intervalo."""
			#return [np.random.choice(list(x),replace = False)]
			return x
		def cost_function(x):
			""" Cost of x = f(x)."""
			return self.f(x)
		
		def random_vecino(x= None, fraction= 1):
			"""Move a little bit x, from the left or the right."""
			def nodos(): return swap(x)
			def pesos(): return swap(x)

			if c_nodes: return nodos()
			elif c_weight: return pesos()

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
		def pesos():
			state = random_start(interval)
			cost = cost_function(state)
			states, costs = [state], [cost]
			for step in range(self._maxsteps):
				self._digraph = CurrencyDigraph(self._tipo, self._filename, self._password, self._filtro, self._currency, rnd = self._rnd, log= self._log)
				fraction = step / float(self._maxsteps)
				T = temperature(fraction)
				new_state = random_vecino(state, fraction)
				new_cost = cost_function(swap(new_state))
				if debug: print(f"Step #{step}/{self._maxsteps} : T = {T}, state = {state}, cost = {cost}, new_state = {new_state}, new_cost = {new_cost}")
				if acceptance_probability(cost, new_cost, T) > np.random.random():
					state, cost = new_state, new_cost
					states.append(state)
					costs.append(cost)
				if state != new_state:
					pass
			return state, cost_function(state), states, costs

		def nodos():
			state = random_start(interval)
			cost = cost_function(self._digraph.weights)
			states, costs = [state], [cost]
			nuevos_caminos = []
			for step in range(self._maxsteps):
				self._digraph = CurrencyDigraph(self._tipo, self._filename, self._password, self._filtro, self._currency, rnd = self._rnd, log= self._log)
				fraction = step / float(self._maxsteps)
				T = temperature(fraction)
				new_state = random_vecino(state, fraction)
				nuevos_caminos.append(self._digraph.scraper.scrape(set(new_state)))
				new_cost = cost_function(nuevos_caminos[-1])
				if debug: print(f"Step #{step}/{self._maxsteps} : T = {T}, state = {state}, cost = {cost}, new_state = {new_state}, new_cost = {new_cost}")
				if state != new_state:
					print('.')
				if acceptance_probability(cost, new_cost, T) > np.random.random():
					state, cost = new_state, new_cost
					states.append(state)
					costs.append(cost)
			return state, cost_function(state), states, costs
		
		if c_nodes:
			return nodos()
		elif c_weight:
			return pesos()
