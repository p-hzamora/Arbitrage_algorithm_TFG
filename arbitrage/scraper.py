from arbitrage.parameter import Parameter
from arbitrage.keyGenerator import KeyGenerator as KG
from arbitrage.errors import errorTipo, FileNameError

import os, shutil, requests, concurrent.futures #Para hacer consultas con multihilo
import numpy as np
import pandas as pd
from datetime import datetime
import random as rn

class Scraper(Parameter):
	Pmonedas = []
	Nmonedas = []
	def __init__(self, tipo, filename, password, filtro, rnd, log):
		super().__init__(tipo, filename, password, filtro, rnd, log)
		self._data = any
		self._monedas = []
		self._ruta = os.path.join(os.getcwd(),'arbitrage', 'files', filename)
		if filename not in os.listdir(os.sep.join(self._ruta.split(os.sep)[:-1])): self._ruta = os.path.join(os.getcwd(),'arbitrage','exchangerate', filename) 
		self._rates = {}
		self._strs = {}
		self._keys = {}
		self._key = 0
		self._matrix_exchanges = self.get_rates(self._tipo, self._filtro)	#Devuelve una matriz numpy()
		self.scrape()	# Las variables se convierten a logaritmo
 
	@property
	def monedas(self):
		return self._monedas

	@property
	def password(self):
		return self._password

	@property
	def matrix_exchanges(self):
		return self._matrix_exchanges

	def get_rates(self, tipo , filtro):
		'''
		Metodo para extraer los valores de la API
  		'https://v6.exchangerate-api.com/v6/_________}/latest/___'
    	'''
		def get_values(url,	clave = None):
			data = requests.get(url,timeout=10)
			if data.status_code != 200:
				self._password = KG.get_key_api()
				url = lambda password= None, DE= None: f'https://v6.exchangerate-api.com/v6/{password}/latest/{DE}'
				return get_values(url(self._password,DE),'conversion_rates')
			if clave == None:
				return data.json()
			else:
				return data.json()[clave]

		def values_by_API():
			'''
			Devuelve un self._data con todas las posibles combinaciones entre distintas monedas
			A parte se encarga de rellenar la variable self._matrix_exchanges
			'''
			def multihilo(API_data):
				'''
				Ordena los datos obtenidos de la API
				args API_data:	lista de diccionarios [dict(),dict23(),dict3()]
    			'''
				matrix_total = np.zeros((self._key,self._key))		#Array de ceros np.zeros(rows,columns)
				for row in API_data:								#Se trata de una lista ordenada
					for x, val in list(row.items()):
						matrix_total[self._strs[list(row)[0]]][self._strs[x]] = val
				return matrix_total

			def get_API_lenta(x):
				rates = get_values(url(self._password,x),'conversion_rates')
				valores = []
				for val in rates.values():
					valores.append(val)
				temp = valores[0]
				del valores[0]
				valores.insert(self._strs[x],temp)
				return valores

			#ACCESO API CON MULTIHILO
			with concurrent.futures.ThreadPoolExecutor() as executor:
				futures = []
				for moneda in self._strs:
					futures.append(executor.submit(get_values, url = url(self._password,moneda), clave = 'conversion_rates'))
			#lista de cada extraccion sacada de la API
			extraccion = [ future.result() for future in concurrent.futures.as_completed(futures)]
			matrix_total = multihilo(extraccion)
			self._matrix_exchanges = matrix_total

			# #ACCESO API LENTA se accede a los valores uno a uno (160 peticiones a la web en cola)
			# matrix_total = []
			# for x in self._strs:
			# 	matrix_total.append(get_API_lenta(x))
			#self._matrix_exchanges = matrix_total
   

			#CREAMOS Dataframe
			df = pd.DataFrame(matrix_total, columns = self._strs, index= self._strs)
			df.to_csv(self._ruta)

			#Si no existe copia de seguridad se crea
			fecha_larga = datetime.today().strftime('%m.%d.%Y')
			fecha_corta = fecha_larga[:-4] + fecha_larga[-2:]
			name =fecha_corta + '.csv'
			new_path = os.path.join(os.getcwd(),'arbitrage','exchangerate')
			if name not in set(os.listdir(new_path)):
				shutil.copyfile(self._ruta, os.path.join(new_path, name))
			return df

		def values_by_csv():
			if not self._filename.endswith('.csv'): raise FileNameError
			df = pd.read_csv(self._ruta, index_col = 0 , encoding='utf-8')
			if filtro == None:
				return df
			else:
				filas = columnas = filtro
				df = df.loc[filas, columnas]
				return df

		def values_by_excel():
			if not self._filename.endswith('.xlsx'): raise FileNameError
			df = pd.read_excel(self._ruta, index_col = 0, sheet_name= 'datos').fillna('-')	# fillna(np.inf) para probar los excels y ver si funciona el programa
			if filtro == None:
				return df
			else:
				filas = columnas = filtro
				df = df.loc[filas, columnas]
				return df

		if tipo.lower() == 'csv':
			self._data = values_by_csv()
   
		elif tipo.lower() == 'api':
			DE = 'AED'
			url = lambda password =self._password,DE = None: f'https://v6.exchangerate-api.com/v6/{password}/latest/{DE}'

			dict_values = get_values(url(self._password,DE),'conversion_rates')  #dict {"MONEDA": VALOR,····}
			self._keys ={pos: palabra for pos,palabra in enumerate(tuple([x for x in dict_values.keys()]))}
			self._strs= {llave: num for num,llave in self._keys.items()}
			self._key = len(self._keys)
			self._monedas = set(self._keys.values())

			self._data = values_by_API()

		elif tipo == 'xlsx':
			self._data = values_by_excel()
		else:
			raise errorTipo
		if tipo != 'api':
			self._keys ={pos: palabra for pos,palabra in enumerate(tuple([x for x in self._data.columns]))}
			self._strs= {llave: num for num,llave in self._keys.items()}
			self._key = len(self._keys)
			self._monedas = set(self._keys.values())
		return self._data.to_numpy()

	def scrape(self):
		'''
		Metodo para inicializar todos los caminos entre divisas
		returns: self.rates
		'''
		for row in self._monedas:
			for column in self._monedas:
				if self._log == True: val = -np.log(self._matrix_exchanges[self._strs[row]][self._strs[column]]) 	# para calcular Bellman-Ford para casos de arbitraje		
				else:val = self.matrix_exchanges[self._strs[row]][self._strs[column]]				# Para calcular Bellman-Ford directamente con los pesos del problema
				if val == 0:
					val = np.inf
				self._rates[(row,column)] = val
		return self._rates

	def test_arbitrage(self, accuracy = 0.01):
		'''
		Devuelve tres valores para hacer pruebas:
		return: self._matrix_exchanges
				1/ self._matrix_exchanges
				array de diferencias
  		'''
		n= self._matrix_exchanges.size
		arr = self._matrix_exchanges
		arrT = -1/self._matrix_exchanges.transpose()
		arr_beneficios = abs(arr + arrT)
		total = 0
		for fila, x in enumerate(arr_beneficios):
			for columna, y in enumerate(x):
				if y > accuracy:
					#print(f"{self._keys[fila]}/{self._keys[columna]} = {y}")
					total +=1
		print_arr = pd.DataFrame(arr_beneficios, index = self._strs, columns= self._strs)
		print('Porcentaje de cambio de divisas distinto de 0: {:.03f}%'.format(total/n*100))
		return arr, arrT, print_arr

	def set_rnd_monedas(self):

		def swap():
			'''
			Realizar un unico intercambio entre 2 valores del diccionario
			'''
			if any((isinstance(self._monedas,list),isinstance(self._monedas,set))):
				self._monedas = list(self._monedas)
				lista = np.arange(0,len(self._monedas))
				rdm = (np.random.choice(lista,2,replace= False))
				#realizamos swap
				Scraper.Pmonedas = self._monedas
				temp = self._monedas[rdm[1]]
				self._monedas[rdm[1]] = self._monedas[rdm[0]]
				self._monedas[rdm[0]] = temp
				Scraper.Nmonedas = self._monedas
			return rdm

		if self._rnd:
			order = rn.sample(range(0,len(self._monedas)),len(self._monedas))
			self._monedas = [list(self._monedas)[x] for x in order]
			rdm = None
		else:
			rdm = swap()
		#para obtener el diccionario de pesos cambiado
		self.scrape()
		return rdm

	def print_data(self):
		print(self._data)
		print('\n')

if __name__ == '__main__':
	# example usage
	s = Scraper(tipo = 'csv')
	for _ in range(10):
		s.set_rnd_monedas()
		print(s.monedas)
		print()

