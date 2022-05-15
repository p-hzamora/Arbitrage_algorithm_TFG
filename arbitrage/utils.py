from colorama import init
init()
from colorama import Fore

def printcol(texto,tipo_color):
    '''
    NEGRO
    AZUL
    CIAN
    VERDE
    NEGRO_CLARO
    AZUL_CLARO
    CIAN_CLARO
    VERDE_CLARO
    MAGENTA_CLARO
    ROJO_CLARO
    BLANCO_CLARO
    AMARILLO_CLARO
    MAGENTA
    ROJO
    AMARILLO    
    '''
    diccionario = {
        'NEGRO': 'BLACK',
        'AZUL': 'BLUE',
        'CIAN': 'CYAN',
        'VERDE': 'GREEN',
        'NEGRO_CLARO': 'LIGHTBLACK_EX',
        'AZUL_CLARO': 'LIGHTBLUE_EX',
        'CIAN_CLARO': 'LIGHTCYAN_EX',
        'VERDE_CLARO': 'LIGHTGREEN_EX',
        'MAGENTA_CLARO': 'LIGHTMAGENTA_EX',
        'ROJO_CLARO': 'LIGHTRED_EX',
        'BLANCO_CLARO': 'LIGHTWHITE_EX',
        'AMARILLO_CLARO': 'LIGHTYELLOW_EX',
        'MAGENTA': 'MAGENTA',
        'ROJO': 'RED',
        'AMARILLO': 'YELLOW'
    }
    tipo_color = diccionario[tipo_color]
    colores = dict(Fore.__dict__.items())
    #[print(colores[el] + f"{el}") for el in colores.keys()]
    a = print(colores[tipo_color] + f"{texto}" + Fore.RESET)
    return a
