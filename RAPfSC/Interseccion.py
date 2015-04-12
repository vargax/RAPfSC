# -*- coding: utf-8 -*-
__author__ = 'cvargasc'

# Una intersección es un SignalController, tiene carriles de entrada, salida, cruces y semáforos.
class Interseccion:

    # ------------------------
    # Atributos
    # ------------------------
    # Cada carril tiene un ID definido por su coordenada y una ocupación.
    # La ocupación se define como la razón entre de carros en el carril y la máxima cantidad de carros vista en el carril
    #  |-> Debe ser un número entre 0 y 1
    carrilesEntrada = {}  # La coordenada de los carriles de entrada hacen referencia al origen de los vehículos
    carrilesSalida = {}   # La coordenada de los carriles de salida hacen referencia al destino de los vehículos

    # Para calcular las ocupaciones necesito guardar también el máximo de vehículos vistos
    maxVhCarrilesEntrada = {}  # La cantidad máxima de vehículos vista en ese carril de entrada
    maxVhCarrilesSalida = {}   # La cantidad máxima de vehículos vista en ese carril de salida

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
        self.id = sc.AttValue('Name')  # Recupero y guardo el ID del SignalController
        print " + Instanciando Interseccion para SignalController "+self.id

        # Voy a generar los cruces a partir de los SignalGroups
        for sg in sc.SGs:
            id = sg.AttValue('Name')
            print "\n  ++ Generando Cruce para SignalGroup "+id
            carrilEntrada, carrilesSalida = id.split(';')[0],id.split(';')[1].split(':')

            if not carrilEntrada in self.carrilesEntrada:
                print "   +++ Generando el carril de entrada "+carrilEntrada
                self.carrilesEntrada[carrilEntrada] = -1 # La ocupación de cada carril de entrada se inicializa en -1
                self.maxVhCarrilesEntrada[carrilEntrada] = 1 # La cantidad máxima de vehículos vistos en ese carril se inicializa en 1

            for carrilSalida in carrilesSalida:
                if not carrilSalida in self.carrilesSalida:
                    print "   +++ Generando el carril de salida "+carrilSalida
                    self.carrilesSalida[carrilSalida] = -1 # La ocupación de cada carril de salida se inicializa en -1
                    self.maxVhCarrilesSalida[carrilSalida] = 1 # La cantidad máxima de vehículos vistos en ese carril se inicializa en 1

            self.cruces[id] = [sg,carrilEntrada,carrilesSalida]

        print "\n + Instanciada Interseccion "+self.id+" :: \n    Cruces="+str(len(self.cruces))\
              + "\n    Carriles Entrada=" + str(len(self.carrilesEntrada))\
              + "\n    Carriles Salida=" + str(len(self.carrilesSalida))








