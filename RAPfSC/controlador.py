# -*- coding: utf-8 -*-
__author__ = 'cvargasc'
# ------------------------
# Imports
# ------------------------
import win32com.client as com
import os
from modelo import Interseccion
from escenario import Ocupacion

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
    id = sc.AttValue('Name')
    idVissim = str(sc.AttValue('No'))
    print " \n+Procesando SignalController '"+id+"' ..."
    intersecciones[id] = Interseccion(sc)
    #for sg in sc.SGs:
    #    print "SignalGroup :: No: "+idVissim+"-"+str(sg.AttValue('No'))+" | Name: "+str(sg.AttValue("Name"))

#for se in vissim.Net.SignalHeads:
#    print "SignalHead :: No: "+str(se.AttValue("No"))+" | Lane: "+str(se.AttValue("Lane"))+" | SG: "+str(se.AttValue("SG"))

print "\nRecuperadas "+str(len(intersecciones))+" intersecciones de la red '"+RED+"'"

for iteracion in range(1,ITERACIONES):
    print "Iteración "+str(iteracion)+"\n"
    vissim.Simulation.SetAttValue('SimBreakAt', iteracion*PASOS_ENTRE_ITERACIONES)
    vissim.Simulation.RunContinuous()
    Ocupacion.actualizarOcupacion()