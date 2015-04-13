import Interseccion

__author__ = 'tizon'


class ModeloSolucion:
    # relacion carriles entrada/salida: 1 mismo flujo; < 1 carril salida congestionado
    # Interseccion.carrilesEntrada

    listPrioridadesCruces = {}
    listPrioridadesGrupos = {}

    def _optimizarInterseccion(self):
        #primero recorre los cruces para crear directorio de ocupaciones del cruce(es decir prioridad del cruce)
        self.__recorrerCruces()
        #Luego recorre los grupos que tienen cruces (cruces pueden estar contenidos en 1 o mas grupos), para definir prioridad por grupo
        self._recorrerGrupos()
        #por ultimo escoge  grupo con la mayor prioridad
        #estara definido por cantidad de cruces que tenga el grupo la sumatoria de sus prioridades, si hay prioridades no comparables se tomara el que tenga mas cruces
        #prioridad estara definida entre 0 y 1
        self._maximizarPrioridad()


    def __recorrerCruces(self):
        for id,cruce in Interseccion.cruces.items():
            cruce[0].SetAttValue("State","RED")#signal controller: todos los cruces se ponen en rojo para que al final solo quede activado el grupo de cruces prioritarios
            idEntrada = cruce[1] #"id" del carril de entrada
            listSalida=cruce[2] #lista de carriles de salida
            ## recorre los carriles de salida (1-ocupacion) sera su capacidad de recibir carros
            ## cEntrada.ocupacion sera el flujo que necesita pasar
            ## rest.. cEntrada<=1-sum((i),cSalida(i).ocupacion)
            ## prioridad=((cEntrada+(1-csalida))*cEntrada)/maximo
            sumCapacidadSalida=0
            for idSalida in listSalida.items():
                socupacion=Interseccion.carrilesSalida[id]#ocupacion entre 0 y 1
                scapacidad=1-socupacion #la capaciidad de un carril de salida
                sumCapacidadSalida+=scapacidad

             ## calculamos la maxima prioridad entre el carril de entrada y todos sus carriles salida VER archivo GAMS
            max=((10**len(listSalida))+10)*10
            ## calculamos prioridad de cruce
            cEntrada=Interseccion.carrilesEntrada[idEntrada]
            prioridad=((sumCapacidadSalida+cEntrada)*cEntrada)/max
            ##agregamos al diccionario id del cruce como llave y su prioridad
            self.listPrioridadesCruces[id]=prioridad

    def _recorrerGrupos(self):

        #recorre los grupos que es una lista de cruces
        for id,crucesGrupo in Interseccion.grupos.item():
            ##recorre los cruces del grupo n
            sumPrioridad=0
            for idcruce in crucesGrupo.items():
                ##devuelve la prioridad ya caculada del cruce
                prioridad=self._darPrioridadCruce(idcruce)
                ##se suman las prioridades
                sumPrioridad+=prioridad
            self.listPrioridadesGrupos[id]=sumPrioridad

    def _maximizarPrioridad(self):
        idGrupoMaximo=''
        maxprioridad=0

        for idGrupo,prioridad in self.listPrioridadesGrupos:
            if prioridad > maxprioridad:
                idGrupoMaximo=idGrupo
                maxprioridad=prioridad
            elif prioridad == maxprioridad:
                ##si hay igualdad en prioridades se escoge el grupo con mayor cruces
                #cantidad de cruces del grupo que fue igual al grupo maximo
                tamCrucesGrupo=len(Interseccion.grupos[idGrupo][0])
                #cantidad de cruces del grupo maximo guardado anteriormente
                tamCrucesGrupoMaximo=len(Interseccion.grupos[idGrupoMaximo][0])
                if tamCrucesGrupoMaximo < tamCrucesGrupo:
                    #si hay un grupo con mayor prioridad se reemplaza por el anterior
                     idGrupoMaximo=idGrupo
                     maxprioridad=prioridad
            elif prioridad == 0 and prioridad==maxprioridad:
                #si casualmente el primer gurpo tiene tambn prioridad 0 entonces se reemplaza por los valores defaults para no errores
                      idGrupoMaximo=idGrupo
                      maxprioridad=prioridad

        self._activarGrupo(idGrupoMaximo)


    def _darPrioridadCruce(self,id):
        return self.listPrioridadesCruces[id]

    def _darPrioridadGrupo(self,id):
        return self.listPrioridadesGrupos[id]

    def _activarGrupo(self,idgrupo):
        cruces=Interseccion.grupos[idgrupo]
        for id,cruce in cruces.item():
             cruce[0].SetAttValue("State","GREEN")#signal controller: todos los cruces del grupo se ponen en verde:grupo con mayor prioridad












