# class Padre():
#     NUM = None
#     def __init__(self,numero= 0):
#         Padre.NUM = numero
    
#     @property
#     def numero(self):
#         return Padre.NUM

    
#     @classmethod
#     def change(clss, a):
#         Padre.NUM = a


# class Hijo():
#     def __init__(self,numero):
#         self._numero_hijo = numero
    
#     @property
#     def numero(self):
#         return self._numero_hijo

#     def cambiar(self):
#         Padre.change(self._numero_hijo)
    

# hijo = Hijo(10)
# padre = Padre()

# print(f"Numero de hijo {hijo.numero}")
# print(f"Numero de padre {padre.numero}")
# hijo.cambiar()
# print(f"Numero de hijo {hijo.numero}")
# print(f"Numero de padre {padre.numero}")


class Padre():
    asdf = None
    def __init__(self,numero= 0):
        self._numero = numero

    @property
    def numero(self):
        return self._numero

    
    @classmethod
    def change(cls, a):
        Padre.asdf = a
        cls.numero = a

class Hijo(Padre):
    def __init__(self,numero):
        super().__init__(numero)


hijo = Hijo(10)

print(Padre.asdf)
print(f"Numero de hijo {hijo.numero}")
hijo.change(20)
print(f"Numero de hijo {hijo.numero}")
print(Padre.asdf)
