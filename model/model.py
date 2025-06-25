import copy

import networkx as nx
from database.DAO import DAO
from model.album import Album


class Model:
    def __init__(self):
        self.grafo=nx.Graph()
        self.idMap = {}
        self.bestSet=[]
        self.albumNew=None

    def buildGraph(self,durata):
        nodi=DAO.getNodes()
        for n in nodi:
            if n.durata>durata:
                self.grafo.add_node(n)
        for n2 in self.grafo.nodes:
            self.idMap[n2.AlbumId]=n2

        edges=DAO.getEdges(self.idMap)
        for e in edges:
            self.grafo.add_edge(e[0],e[1])


    def getNumNodes(self):
        return len(list(self.grafo.nodes))


    def getNumEdges(self):
        return len(list(self.grafo.edges))

    def getNodes(self):
        return list(self.grafo.nodes)

    def getCompConn(self,album):
        albumNew=None
        for n in self.idMap:
            if album==self.idMap[n].Title:
                albumNew=self.idMap[n]
        componente=list(nx.node_connected_component(self.grafo,albumNew))
        durataTot=0
        for nodo in componente:
            durataTot=durataTot+nodo.durata
        return durataTot,len(componente)

    def getSetAlbum(self,durataTot,album):
        self.bestSet = []
        self.albumNew = None
        for n in self.idMap:
            if album == self.idMap[n].Title:
                self.albumNew = self.idMap[n]
        parziale=[self.albumNew]
        componente = list(nx.node_connected_component(self.grafo, self.albumNew))
        componente.remove(self.albumNew)
        for nodo in componente:
            componente.remove(nodo)
            parziale.append(nodo)
            self.ricorsione(parziale,componente,durataTot)
            componente.remove(nodo)
            parziale.append(nodo)

        return self.bestSet

    def ricorsione(self,parziale,rimanenti: list[Album],durataTot):
        if self.durataAlbum(parziale)>durataTot:
            return

        if len(parziale)>len(self.bestSet):
            self.bestSet=copy.deepcopy(parziale)

        for n in rimanenti:
            parziale.append(n)
            rimanenti.remove(n)
            self.ricorsione(parziale,rimanenti,durataTot)
            parziale.remove(n)
            rimanenti.append(n)



    def durataAlbum(self,set):
        durataAlbum = 0
        for album in set:
            durataAlbum = durataAlbum + album.durata
        return durataAlbum
