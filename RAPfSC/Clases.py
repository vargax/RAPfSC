# -*- coding: utf-8 -*-
__author__ = 'cvargasc'
import copy

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
    # cruce[1] --> String que contiene el ID del carril de entrada
    # cruce[2] --> Lista de Strings con los identificadores de los carriles de salida
    #####
    # Por ejemplo para cambiar el color del semáforo asociado al SignalGruop del cruce '0,-1;0,1:1,0'
    # cruces['0,-1;0,1:1,0'][0].SetAttValue("State", "GREEN")
    cruces = {}

    # Conjuntos de cruces que se pueden habilitar simultáneamente
    grupos = {}

    # ------------------------
    # Constructor
    # ------------------------
    # Inicializa la intersección con sus respectivos carriles de entrada, salida y cruces
    # |-> calcula los grupos de cruces compatibles
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

        # Llamo el método para calcular los grupos de cruces que se pueden habilitar simultáneamente
        self.__calcularGrupos()

        print "\n + Instanciada Interseccion "+self.id+" :: \n    Cruces="+str(len(self.cruces))\
              + "\n    Carriles Entrada=" + str(len(self.carrilesEntrada))\
              + "\n    Carriles Salida=" + str(len(self.carrilesSalida))

    # ------------------------
    # Métodos privados
    # ------------------------
    # Método encargado de calcular los grupos de cruces que se pueden habilitar simultáneamente
    def __calcularGrupos(self):
        self.__crucesCompatibles()

    # Dos cruces son compatibles si ninguno de sus segmentos se cortan
    def __crucesCompatibles(self):
        print " ++ Calculando los cruces compatibles..."
        # Para cada cruce voy a ver si es compatible los demás
        cruces = copy.copy(self.cruces)  # Genero una copia del diccionario de cruces
        compatibles = {}  # Diccionario que contiene una lista de cruces compatibles para cada uno de los cruces
        for idCruce, cruce in cruces.items():
            compatibles[idCruce] = [] # Inicializo la lista de cruces compatibles para todos los cruces

        for idCruce, cruce in cruces.items():
            del cruces[idCruce]  # Saco el cruce actual de la lista de cruces que estoy recorriendo

            segmentosCruce = self.__generarSegmentos(idCruce)
            for idCandidato, candidato in cruces.items():
                segmentosCandidato = self.__generarSegmentos(idCandidato)
                sonCompatibles = True

                for segmentoCruce in segmentosCruce:
                    for segmentoCandidato in segmentosCandidato:
                        if self.__segmentosSeCortan(segmentoCruce,segmentoCandidato):
                            sonCompatibles = False
                            break
                    if not sonCompatibles:
                        break

                if not sonCompatibles:
                    break
            else:
                # La compativilidad es simétrica
                compatibles[idCruce].append(idCandidato)
                compatibles[idCandidato].append(idCruce)

        for idCruce, crucesCompatibles in compatibles.items():
            print " +++ El cruce "+idCruce+" cuenta con "+str(len(crucesCompatibles))+" cruces compatibles:"
            print "       ",crucesCompatibles

        return compatibles

    # ------------------------
    # Métodos privados de apoyo
    # ------------------------
    # Evalúa la posición de del punto respecto al segmento calculando el producto cruz / Regla de la mano derecha
    #   Un punto c es una tupla (xc,yc)
    #   Un segmento es una tupla de puntos (a,b) con a = (xa,ya) y b = (xb,yb)
    # Devuelve un float:
    #   Si > 0 -> DERECHA | Si < 0 -> IZQUIERDA | Si = 0 -> Sobre el segmento
    def __posicionPtoRespectoSegmento(self, segmento, punto):
        print "  ++++ Determinando donde se encuentra el punto",punto," respecto al segmento ",segmento
         # Las coordenadas del segmento
        xa,ya = segmento[0]
        xb,yb = segmento[1]

        # Las coordenadas del punto
        xc,yc = punto

        # Producto Cruz
        respuesta = (xc-xa)*(yb-ya) - (xb-xa)*(yc-ya)
        if respuesta < 0:
            print "  ++++ El punto",punto," se encuentra a la IZQUIERDA del segmento ",segmento
        elif respuesta == 0:
            print "  ++++ El punto",punto," se encuentra a la ALINEADO con el segmento ",segmento
        else:
            print "  ++++ El punto",punto," se encuentra a la DERECHA del segmento ",segmento

        return respuesta

    # Un cruce tiene un segmento por cada uno de sus carriles de salida, esta función genera todos los segmentos para
    # el cruce cuyo ID es pasado como parámetro.
    def __generarSegmentos(self, idCruce):
        cruce = self.cruces[idCruce]
        carrilEntrada = cruce[1].split(',')
        carrilEntrada = float(carrilEntrada[0]), float(carrilEntrada[1])
        carrilesSalida = cruce[2]

        segmentos = []
        for carrilSalida in carrilesSalida:
            carrilSalida = carrilSalida.split(',')
            carrilSalida = float(carrilSalida[0]), float(carrilSalida[1])

            segmentos.append((carrilEntrada,carrilSalida))

        print "  ++++ Segmentos generados para el cruce "+idCruce+" :: ",segmentos
        return segmentos

    # Determina si los dos segmentos pasados como parámetro se cortan
    #  Se considera que se cortan si tienen al menos un punto en común (incluidos los extremos)
    #  EXCEPTO Si tienen los dos puntos en común => Si segmento2 es el mismo segmento1 pero en dirección opuesta
    #  EXCEPTO Si el punto de origen es el mismo => Los carros partiendo del mismo carril no se chocan
    #  EXCEPTO Si el punto de origen del primer segmento es igual al punto de destino del segundo segmento Y
    #          el punto de destino del primer segmento está a la izquierda del segundo segmento => No se cortan
    #          si el destino del primer segmento está a la DERECHA del segundo segmento => Cruzar a la derecha
    #
    # Un segmento es una tupla de puntos (a,b) con a = (xa,ya) y b = (xb,yb)
    def __segmentosSeCortan(self,segmento1,segmento2):
        print "  ++++ Determinando si los segmentos ",segmento1," y ",segmento2," se cortan..."
        # Caso en el cual los segmentos son los mismos pero en direcciones opuestas: por ejemplo de norte a sur
        # y de sur a norte
        if segmento1[1] == segmento2[0] and segmento1[0] == segmento2[1]:
            print "        |-> NO se cortan :: Son el mismo en direcciones opuestas..."
            return False  # No se cortan, luego son compatibles

        # Caso en el cual el punto de origen es el mismo: por ejemplo del norte hacia el sur y del norte hacia
        # el occidente
        if segmento1[0] == segmento2[0]:
            print "        |-> NO se cortan :: El punto de origen es el mismo..."
            return False  # Salen del mismo sitio, luego son compatibles

        # Caso en el cual el origen del primer segmento es el destino del segundo, y el destino del primero está
        # a la derecha del segundo: por ejemplo de norte a sur y de sur a occidente ==> Incluye el primer caso!!
        if segmento1[0] == segmento2[1] and self.__posicionPtoRespectoSegmento(segmento2, segmento1[1]) < 0 \
                or segmento1[1] == segmento2[0] and self.__posicionPtoRespectoSegmento(segmento1, segmento2[1]):
            print "        |-> NO se cortan :: Puntos de origen/destino iguales y destino a la derecha..."
            return False

        # Los demás casos:
        posPto1 = self.__posicionPtoRespectoSegmento(segmento2, segmento1[0])
        posPto2 = self.__posicionPtoRespectoSegmento(segmento2, segmento1[1])
        if posPto1*posPto2 <= 0:
            posPto1 = self.__posicionPtoRespectoSegmento(segmento1, segmento2[0])
            posPto2 = self.__posicionPtoRespectoSegmento(segmento1, segmento2[1])
            if posPto1*posPto2 <= 0:
                print "        |-> SI se cortan :: Los segmentos se cortan..."
                return True
        print "        |-> NO se cortan :: Los segmentos no se cortan..."
        return False
