# -*- coding: utf-8 -*-
__author__ = 'cvargasc'

# ------------------------
# Imports
# ------------------------
import win32com.client as com
import os

# ------------------------
# CONSTANTES
# -----------------------
RED = "simpleintersection"

# ------------------------
# SCRIPT
# -----------------------
print "Conectando a VISSIM a través de COM..."
vissim = com.Dispatch("Vissim.Vissim-32.700") # Vissim 7 - 32 bit

rutaRed = os.getcwd()+"\\data\\networks\\"+RED+"\\"+RED+".inpx"
print "Cargando red "+rutaRed+" ..."
vissim.LoadNet(rutaRed)

print "Recuperando SignalControllers..."
for sc in vissim.Net.SignalControllers:
    print " \n+Procesando SignalController '"+sc.AttValue('Name')+"' ..."
    for sg in sc.SGs:
        print " ++Procesando SignalGroup '"+sg.AttValue('Name')+"' ..."

