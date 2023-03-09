import datetime

import numpy as np

def get_month(mes = datetime.datetime.today().month, current_list = False, decrease = 0 ):
    '''
    Funcion para retornar los meses en formato string pasando una lista de los meses que se desean conocer
    var lista: list(1,2,3,4)
        los parametros dentro de la lista son numeros de meses de 1 a 12
        
    par current_list, si lo activamos obtendremos una lista de meses en espanol desde el el primero hasta el actual
    '''
    def spanish(month):
        if month == "January": return 'Enero'
        elif month == "February": return 'Febrero'
        elif month == "March": return 'Marzo'
        elif month == "April": return 'Abril'
        elif month == "May": return 'Mayo'
        elif month == "June": return 'Junio'
        elif month == "July": return 'Julio'
        elif month == "August": return 'Agosto'
        elif month == "September": return 'Septiembre'
        elif month == "October": return 'Octubre'
        elif month == "November": return 'Noviembre'
        elif month == "December": return 'Diciembre'
        
    if current_list != 0: iterador = np.arange(1, mes + 1 + decrease)
    elif isinstance(mes,int) and decrease == 0:iterador = mes, #coma para convertirlo en lista
    elif isinstance(mes,int) and decrease != 0: iterador = (mes + decrease),
    elif isinstance(mes,list): iterador = mes
    else: (mes + decrease)
    
    if mes ==0:
        raise Exception('meses deben estar entre 1..12')
    result = [spanish(datetime.date(2022,month ,1).strftime('%B')) for month in iterador ]
    return ", ".join(result)  

if __name__ == "__main__":
    print(get_month(current_list=True, decrease= -1))