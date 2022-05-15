class errorTipo(Exception):
    def __str__(self):
        return ''' No se conoce el parametro tipo introducido'''
    pass
class FileNameError(Exception):
    def __str__(self):
        return ''' La extension del archivo no coincide con el tipo indicado'''
    pass

class noArbitrage(Exception):
    def __str__(self):
        return "No hay oportunidad de arbitraje pues no hay un ciclo negativo"
    pass

class CantExecuteSimulatedAnnealing(Exception):
    def __str__(self):
        return "No se puede ejecutar este algoritmo pues ocasionaria un bucle infinito"
    pass

class negativeCycleDetected(Exception):
    def __str__(self):
        return "Ciclo negativo detectado"
    pass