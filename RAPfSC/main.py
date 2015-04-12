# -*- coding: utf-8 -*-
__author__ = 'cvargasc'

# ------------------------
# Imports
# ------------------------
import win32com.client as com
from Interseccion import Interseccion
import os

# ------------------------
# CONSTANTES
# -----------------------
RED = "simpleintersection"

# ------------------------
# VARIABLES
# -----------------------
intersecciones = {}

##  --> INIT --> #######################################################
print "Conectando a VISSIM a través de COM..."
vissim = com.Dispatch("Vissim.Vissim-32.700") # Vissim 7 - 32 bit

rutaRed = os.getcwd()+"\\data\\networks\\"+RED+"\\"+RED+".inpx"
print "Cargando red "+rutaRed+" ..."
vissim.LoadNet(rutaRed)

print "\nRecuperando SignalControllers..."
for sc in vissim.Net.SignalControllers:
    id = sc.AttValue('Name')
    print " \n+Procesando SignalController '"+id+"' ..."
    intersecciones[id] = Interseccion(sc)

print "\nRecuperadas "+str(len(intersecciones))+" intersecciones de la red "+RED