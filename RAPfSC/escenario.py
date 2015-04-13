# -*- coding: utf-8 -*-
import random

__author__ = 'cvargasc'

def actualizarOcupaciones(interseccion):
    for idCarrilEntrada in interseccion.carrilesEntrada:
        interseccion.carrilesEntrada[idCarrilEntrada] = random.random()


    for idCarrilSalida in interseccion.carrilesSalida:
        interseccion.carrilesSalida[idCarrilSalida] = random.random()


