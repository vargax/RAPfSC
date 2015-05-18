# -*- coding: utf-8 -*-
__author__ = 'cvargasc'
# ------------------------
# Imports
# ------------------------
import os

import win32com.client as com
import pythoncom

from modelo import Interseccion
from escenario import Ocupacion
from heuristica import ModeloSolucion


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
heuristicas = []

##  --> INIT --> #######################################################
pythoncom.CoInitialize()
print "Conectando a VISSIM a través de COM..."
vissim = com.Dispatch("Vissim.Vissim-32.700") # Vissim 7 - 32 bit
vissimComId = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, vissim)

rutaRed = os.getcwd()+PATH_REDES+RED+"\\"+RED+".inpx"
print "Cargando red "+rutaRed+" ..."
vissim.LoadNet(rutaRed)

print "\nInstanciando Escenario..."
Ocupacion.inicializar(vissimComId)

print "\nRecuperando SignalControllers..."
for sc in vissim.Net.SignalControllers:
    id = str(sc.AttValue('No'))
    nombre = sc.AttValue('Name')

    scComId = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, sc)

    print " \n+Procesando SignalController '"+id+"' ..."
    interseccion = Interseccion(scComId)
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
    heuristicas.append(ModeloSolucion(interseccion))

for iteracion in range(1,ITERACIONES):
    print "Iteración "+str(iteracion)+"\n"
    vissim.Simulation.SetAttValue('SimBreakAt', iteracion*PASOS_ENTRE_ITERACIONES)
    vissim.Simulation.RunContinuous()

    # El escenario actualiza las ocupaciones de los links
    Ocupacion.actualizarOcupacion()
    # La heurística determina el grupo de cruces a habilitar

    # procesos = []
    for modelo in heuristicas:
        modelo.optimizarInterseccion()
        # p = Process(modelo.optimizarInterseccion())
    #     p.start()
    #     procesos.append(p)
    # for p in procesos:
    #     p.join()