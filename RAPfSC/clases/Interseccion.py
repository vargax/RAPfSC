__author__ = 'cvargasc'

# Una intersección es un SignalController, tiene carriles de entrada, salida, cruces y semáforos.
class Interseccion:

    # ------------------------
    # Atributos
    # ------------------------
    # Cada carril tiene un ID definido por su coordenada y una ocupación.
    carrilesEntrada = {}
    carrilesSalida = {}

    # Cada cruce está compuesto por un semáforo (SignalHead), un carril de entrada y un conjunto de carriles de salida
    cruces = {}

    def __init__(self, sc):
        self.sc = sc # Defino el SignalController como un atributo de la clase
        self.id = sc.AttValue('Name') # Recupero y guardo el ID del SignalController





