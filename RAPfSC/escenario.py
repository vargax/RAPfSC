# -*- coding: utf-8 -*-
import random

__author__ = 'cvargasc'

def actualizarOcupaciones(interseccion):
    for idCarrilEntrada, ocupacion in interseccion.carrilesEntrada:
        ocupacion = random.random()

    for idCarrilSalida, ocupacion in interseccion.carrilesSalida:
        ocupacion = random.random()


