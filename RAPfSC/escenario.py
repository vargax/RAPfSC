# -*- coding: utf-8 -*-

__author__ = 'cvargasc'

class Ocupacion:
    # ------------------------
    # CONSTANTES
    # -----------------------
    llaveEntrada = "entrada"
    llaveConector = "conector"
    llaveSalida = "salida"

    # ------------------------
    # ATRIBUTOS GLOBALES
    # -----------------------
    vissim = None # Referencia a la interfaz COM de Vissim

    linksById   = {}    # Diccionario GLOBAL de tripletas indexado por el ID del link --> Necesario para recuperar los datos
    linksByName = {}    # Diccionario GLOBAL de tripletas indexado por el nombre del link --> Es el utilizado en las intersecciones
    # Cada tripleta contiene:
    # |--> pos 0 ocupacion :: La ocupación actual del link, calculada numVh / maxVh
    # |--> pos 1 numVh     :: El número de vehículos actualmente en el link
    # |--> pos 2 maxVh     :: El número máximo de vehículos vistos en el link

    # ------------------------
    # MÉTODOS
    # -----------------------
    # En este método se obtienen los IDs de los links en Vissim y se relacionan con los nombres utilizados en el Modelo
    @staticmethod
    def inicializar(vissim):
        Ocupacion.vissim = vissim
        # El proceso gira en torno a los SignalHeads, los cuales están siempre ubicados sobre un link de
        # tipo CONNECTOR y asociados a un SignalGroup cuyo nombre representa un Cruce en el modelo. Un
        # CONNECTOR está asociado con dos Links (las carriles de entrada y de salida)
        # El procedimiento es:
        # - Recuperar todos los SignalHeads de la red
        # - Para cada SignalHead
        # -- Recuparar el link en el cual está ubicado
        # ---- A partir de ese Link recuperar los ids de los Links From y To
        # -- Recuperar el id del SignalGroup al cual está asociado
        # ---- A partir de este id recuperar el nombre del SignalGroup, el cual representa el cruce en el modelo
        # Con esta información se genera una lista por cada Link (ocupación, numVh, maxVh) y se registra en dos
        # diccionarios, uno indexado por nombre (para recuperarlo desde el modelo) y otro indexado por ID
        # (para actualizarlo desde el escenario)
        # ToDO extender el modelo para soportar carriles de entrada con MÚLTIPLES carriles de salida
        # ToDo :: IDEA para cruces con más de un carril de salida en la RED colocar el SH en el FromLink en lugar de en el CONNECTOR
        for sh in vissim.Net.SignalHeads:
            idConnector = sh.AttValue('Lane').split('-')[0] # Devuelve el id del link en el cual está ubicado el SignalHead
            connector = vissim.Net.Links.ItemByKey(idConnector)  # a partir del ID recupero el elemento
            idFromLink = connector.AttValue('FromLink')          # teniendo el elemento pido el id de FromLink
            idToLink = connector.AttValue('ToLink')              # y el id de ToLink

            # Devuelve idSC-idSG donde idSC es el id del SignalController y idSG es el id del SignalGroup en ese SignalController
            idSC, idSG = sh.AttValue('SG').split('-')
            sc = vissim.Net.SignalControllers.ItemByKey(idSC)
            # Este es el nombre que representa el cruce en el modelo, por ejemplo '0,-1;0,1:1,0'  # ToDO este caso en particular NO está soportado
            nombreSignalGroup = sc.SGs.ItemByKey(idSG).AttValue('Name')
            carrilEntrada, carrilesSalida = nombreSignalGroup.split(';')[0],nombreSignalGroup.split(';')[1].split(':')

            if len(carrilesSalida) != 1:
                raise "Más de un carril de salida aún NO ESTÁ SOPORTADO"

            # Se deben crear tres listas, una por cada uno de los links. Todos se inicializan con ocupación = 0,
            # numVh = 0 y maxVh = 1
            entrada = [0.0,0.0,1.0]
            conector = [0.0,0.0,1.0]
            salida = [0.0,0.0,1.0]

            # Cada lista se registra en los dos diccionarios
            # - El id del link es global en la red --> Solo se requiere un índice
            Ocupacion.linksById[idFromLink] = entrada
            Ocupacion.linksById[idConnector] = conector
            Ocupacion.linksById[idToLink] = salida


            # El nombre del link es local a la intersección
            # - Se debe indexar por intersección
            # - Se deben diferenciar carriles de entrada de carriles de salida
            if idSC not in Ocupacion.linksByName:
                Ocupacion.linksByName[idSC] = {}
                Ocupacion.linksByName[idSC][Ocupacion.llaveEntrada] = {}
                Ocupacion.linksByName[idSC][Ocupacion.llaveConector] = {}
                Ocupacion.linksByName[idSC][Ocupacion.llaveSalida] = {}

            Ocupacion.linksByName[idSC][Ocupacion.llaveEntrada][carrilEntrada] = entrada
            Ocupacion.linksByName[idSC][Ocupacion.llaveConector][nombreSignalGroup] = conector
            Ocupacion.linksByName[idSC][Ocupacion.llaveSalida][carrilesSalida[0]] = salida  # ToDo corregir índice para múltiples carriles de salida

    @staticmethod
    def actualizarOcupacion():
        # Restableciendo numVh a cero para todos los links
        for link in Ocupacion.linksById.itervalues():
            link[1] = 0.0

        atributosVehiculos = Ocupacion.vissim.Net.Vehicles.GetMultipleAttributes(('No', 'Lane'))
        for vehiculo in atributosVehiculos:
            if vehiculo[1] is None:  # Si el vehículo aún no está en un carril
                continue             # continúo con el siguiente vehículo

            idLink, carrilNum = vehiculo[1].split('-')
            # Implementado bajo EAFP https://docs.python.org/2/glossary.html#term-eafp
            try:
                Ocupacion.linksById[idLink][1] += 1.0
            except KeyError:
                print "++ !! Registro TARDIO del link "+ idLink
                Ocupacion.linksById[idLink] = [0.0,1.0,1.0]

        # Actualizando la ocupación de cada link
        for link in Ocupacion.linksById.itervalues():
            if link[1] > link[2]:
                link[2] = link[1]
            link[0] = link[1]/link[2]

        #print Ocupacion.linksByName