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
    # cruces[ID] --> El ID de un cruce es del estilo: 0,1;0,-1:-1,0 Devuelve lista con los elementos del cruce:
    # cruce[0] --> Signal controller de la interfaz COM
    # cruce[1] --> String que contiene el ID del carril de entra
    # cruce[2] --> Lista de Strings con los identificadores de los carriles de salida
    #####
    # Por ejemplo para cambiar el color del semáforo asociado al SignalGruop del cruce '0,-1;0,1:1,0'
    # cruces['0,-1;0,1:1,0'][0].SetAttValue("State", "GREEN")
    cruces = {}

    # Conjuntos de cruces que se pueden habilitar simultáneamente
    grupos = {}

    def __init__(self, sc):
        self.sc = sc # Defino el SignalController como un atributo de la clase
        self.id = sc.AttValue('Name') # Recupero y guardo el ID del SignalController

        # Voy a generar los cruces a partir de los SignalGroups
        for sg in sc.SGs:
            id = sg.AttValue('Name')
            carrilEntrada =







