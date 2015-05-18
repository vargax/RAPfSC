# -*- coding: utf-8 -*-
__author__ = 'cvargasc'
# ------------------------
# Imports
# ------------------------
import os

import win32com.client as com

from modelo import Interseccion
from escenario import Ocupacion
from heuristica import ModeloSolucion
from multiprocessing import Pool


# ------------------------
# CONSTANTES
# -----------------------
PATH_REDES = "\\data\\networks\\"

#RED = "simpleintersection"
RED = "wdcsmallgrid"

ITERACIONES = 100
PASOS_ENTRE_ITERACIONES = 10
# ------------------------
# VARIABLES
# -----------------------
intersecciones = {}
listModelosSolucion = []

##  --> INIT --> #######################################################
print "Conectando a VISSIM a través de COM..."
vissim = com.Dispatch("Vissim.Vissim-32.700") # Vissim 7 - 32 bit

rutaRed = os.getcwd()+PATH_REDES+RED+"\\"+RED+".inpx"
print "Cargando red "+rutaRed+" ..."
vissim.LoadNet(rutaRed)

print "\nInstanciando Escenario..."
Ocupacion.inicializar(vissim)

print "\nRecuperando SignalControllers..."
for sc in vissim.Net.SignalControllers:
    id = str(sc.AttValue('No'))
    nombre = sc.AttValue('Name')

    print " \n+Procesando SignalController '"+id+"' ..."
    interseccion = Interseccion(sc)
    intersecciones[id] = interseccion # Registro la intersección en el diccionario...

    print " \n++Vinculando SignalController con sus links en el escenario..."
    carrilesEntrada = Ocupacion.linksByName[id][Ocupacion.llaveEntrada]
    conectores = Ocupacion.linksByName[id][Ocupacion.llaveConector]
    carrilesSalida = Ocupacion.linksByName[id][Ocupacion.llaveSalida]
    # ToDo ajustar para múltiples carriles de salida
    interseccion.vincularCarrilesEscenario(carrilesEntrada,conectores,carrilesSalida)

    #for sg in sc.SGs:
    #    print "SignalGroup :: No: "+idVissim+"-"+str(sg.AttValue('No'))+" | Name: "+str(sg.AttValue("Name"))

#for sh in vissim.Net.SignalHeads:
#    print "SignalHead :: No: "+str(sh.AttValue("No"))+" | Lane: "+str(sh.AttValue("Lane"))+" | SG: "+str(sh.AttValue("SG"))

print "\nRecuperadas "+str(len(intersecciones))+" intersecciones de la red '"+RED+"'"



for idInterseccion,interseccion in intersecciones.iteritems():
    listModelosSolucion.append(ModeloSolucion(interseccion))

for iteracion in range(1,ITERACIONES):
    print "Iteración "+str(iteracion)+"\n"
    vissim.Simulation.SetAttValue('SimBreakAt', iteracion*PASOS_ENTRE_ITERACIONES)
    vissim.Simulation.RunContinuous()

    # El escenario actualiza las ocupaciones de los links
    Ocupacion.actualizarOcupacion()
    # La heurística determina el grupo de cruces a habilitar
    #pool=Pool(processes=9)
    for modelo in listModelosSolucion:
       modelo.optimizarInterseccion()


