from arbitrage.parameter import Parameter
from arbitrage.scraper import Scraper

from collections import defaultdict
import numpy as np

class CurrencyDigraph(Parameter):
	def __init__(self, tipo, filename, password, filtro, src, rnd, log):
		super().__init__(tipo, filename, password, filtro, rnd, log)
		self._src = src
		self.graph = defaultdict(list)
		# initializes a scraper object to scrape data
		self.scraper = Scraper(self._tipo,self._filename, self._password, self._filtro, self._rnd, self._log )
		self._password = self.scraper.password
		self.weights = self.scraper._rates
		self.generate_graph()
		self.predecesora = {}
		self._distances = {vertex: np.inf for vertex in self.graph}
		if src:
			self.set_source(src)	#Le damos el nodo por el que queremos calcular el camino critico
		self.print_cache = []
		self.items_per_line = 4
		self.cycles = []
  
	def print_graph(self):
		[print(x,'->', y) for x,y in self.graph.items()]
		print()
		return 
  
	def print_distances(self):
		[print(x, '->', y) for x, y in sorted(self._distances.items())]
		print()
     
	@property
	def pesos(self):
			return self.weights

	def set_source(self, src):
		"""
		Metodo para dotar el inicio de la red
		:returns: void
		"""
		self._distances[src] = 0.0
		return 0

	def generate_graph(self):
		"""
		Metodo para generar el grafo con los datos de la extraccion
		self.graph =  dict() diccionario de todas las interacciones entre nodos
						values = el nodo inicial (u)
						keys = lista de los nodos sucesores (v)
				
		generating an adjacency list and a hashmap of edges that stores
		hashed (u, v) tuples as keys and their respective weights as values
		
		:returns: void
		"""

		for r in self.scraper._rates :
			if 	isinstance(self.weights[r],float) or\
				isinstance(self.weights[r],int):
				self.graph[r[0]].append(r[1]) 
		return self.graph
			
	def find_cycle(self, v):
		"""		
		:param v: ultimo valor de la cadena. 
  				En nuestro caso siempre sera la moneda inicial.
      			Si se llama a esta funcion es porque ha encontrado un ciclo negativo que retornar.
       
		:param predecesora: dict 
  			clave = sucesor	
      		valor = predecesor
        	[+] EUR ---> JPY   	print(self.predecesora['JPY'])
									# EUR
		:returns: list
		"""
		V, res = set(), []
		while v not in V:
			V.add(v)	#para no repetir la misma moneda 
			res.append(v)
			v = self.predecesora[self.scraper._keys[v]]
			v = self.scraper._strs[v]
		path = res[res.index(v):][::-1]
		self.cycles.append(path)
		return path  

	def currencies_to_list(self):
		'''
		Ordenar el diccionario de datos, pero ya esta ordenado con esta nueva API 
		'''
		return sorted([[k,v] for k,v in self.scraper._strs.items()],key = lambda x: x[1])

	@classmethod
	def rnd_weights(cls):
		np.random.sample