# -*- coding: utf-8 -*-
__author__ = 'tizon'
class ModeloSolucion:
    # relacion carriles entrada/salida: 1 mismo flujo; < 1 carril salida congestionado
    # Interseccion.carrilesEntrada

    listPrioridadesCruces = {}
    listPrioridadesGrupos = {}
    idGrupoGanadorAnterior= ''
    prioridadGrupoAnterior= 0.0

    def __init__(self, interseccion):
        self.interseccion = interseccion

    def optimizarInterseccion(self):
         print "Optimizando la interseccion ",self.interseccion.id
        #primero recorre los cruces para crear directorio de ocupaciones del cruce(es decir prioridad del cruce)
         self.__recorrerCruces()
        #Luego recorre los grupos que tienen cruces (cruces pueden estar contenidos en 1 o mas grupos), para definir prioridad por grupo
         self._recorrerGrupos()
        # por ultimo escoge  grupo con la mayor prioridad
        #estara definido por cantidad de cruces que tenga el grupo la sumatoria de sus prioridades, si hay prioridades no comparables se tomara el que tenga mas cruces
        #prioridad estara definida entre 0 y 1
      #  self._maximizarPrioridad()


    def __recorrerCruces(self):
        for id,cruce in self.interseccion.cruces.items():
            idEntrada = cruce[1] #"id" del carril de entrada
            listSalida=cruce[2] #lista de carriles de salida
            ## recorre los carriles de salida (1-ocupacion) sera su capacidad de recibir carros
            ## cEntrada.ocupacion sera el flujo que necesita pasar
            ## rest.. cEntrada<=1-sum((i),cSalida(i).ocupacion)
            ## prioridad=((cEntrada+(1-csalida))*cEntrada)/maximo
            minCapacidadSalida=2
            for idSalida in listSalida:
              #      for id,carriles in self.interseccion.carrilesSalida.items():
            # print id+" vs lista salida:"+idSalida
             socupacion=self.interseccion.carrilesSalida[idSalida][0]#ocupacion entre 0 y 1
             print idSalida +" vs lista salida:"+ str(socupacion)
             scapacidad=1-socupacion #la capaciidad de un carril de salida
             if scapacidad < minCapacidadSalida:
                 minCapacidadSalida=min(minCapacidadSalida,scapacidad)


             ## calculamos la maxima prioridad entre el carril de entrada y el minimo carril de gams VER archivo GAMS
            cEntrada=self.interseccion.carrilesEntrada[idEntrada][0]
            cConector= self.interseccion.conectores[id][0]
            cOcupEnCon=(cEntrada+cConector)
            print "$$$ cconector: " +str(cConector) + "### centrada: " + str(cEntrada)+ " mincapacidad "+ str(minCapacidadSalida)

            prioridad = self.__calcularPrioridad(cOcupEnCon,minCapacidadSalida)

            ##agregamos al diccionario id del cruce como llave y su prioridad
            print "### el cruce: "+ id+ "tiene una prioridad de" + str(prioridad)
            self.listPrioridadesCruces[id]=prioridad

    def __calcularPrioridad(self,entrada,salida):

            max=6.0
            ## calculamos prioridad de cruce
            prioridad=((salida + entrada)*(entrada))/max
            return prioridad

    def _recorrerGrupos(self):
        idGrupoMaximo=''
        maxprioridad=0.0
        #recorre los grupos que es una lista de cruces
        for id,crucesGrupo in self.interseccion.grupos.items():
            ##recorre los cruces del grupo n
            sumPrioridad=0.0
            for idcruce in crucesGrupo:
                ##devuelve la prioridad ya caculada del cruce
                prioridad=self._darPrioridadCruce(idcruce)
                ##se suman las prioridades
                sumPrioridad+=prioridad
            #print "### el grupo"+str(id)+" tiene una prioridad "+ str(sumPrioridad)
            self.listPrioridadesGrupos[id]=sumPrioridad

            ##maximiza el grupo con mayor prioridad

            prioridad=sumPrioridad
            if prioridad > maxprioridad:
                idGrupoMaximo=id
                maxprioridad=prioridad
            elif prioridad == 0 and prioridad==maxprioridad:
                #si casualmente el primer gurpo tiene tambn prioridad 0 entonces se reemplaza por los valores defaults para no errores
                idGrupoMaximo=id
                maxprioridad=prioridad
            #elif id == self.idGrupoGanadorAnterior:
            #    continue
            elif prioridad == maxprioridad:
                ##si hay igualdad en prioridades se escoge el grupo con mayor cruces
                #cantidad de cruces del grupo que fue igual al grupo maximo
                tamCrucesGrupo=len(crucesGrupo)
                #cantidad de cruces del grupo maximo guardado anteriormente
                tamCrucesGrupoMaximo=len(self.interseccion.grupos[idGrupoMaximo][0])
                if tamCrucesGrupoMaximo < tamCrucesGrupo:
                    #si hay un grupo con mayor prioridad se reemplaza por el anterior
                     idGrupoMaximo=id
                     maxprioridad=prioridad
        self.idGrupoGanadorAnterior = idGrupoMaximo
        self.prioridadGrupoAnterior = maxprioridad
        print "El id del grupo ganador: "+str(idGrupoMaximo)+" Y con prioridad: "+ str(maxprioridad)
        self._activarGrupo(idGrupoMaximo)




    def _darPrioridadCruce(self,id):
        return self.listPrioridadesCruces[id]

    def _darPrioridadGrupo(self,id):
        return self.listPrioridadesGrupos[id]

    def _activarGrupo(self,idgrupo):
        if idgrupo!='':
          self.interseccion.habilitarGrupo(idgrupo)
        else:
          print "NO HAY GRUPOS DISPONIBLES"