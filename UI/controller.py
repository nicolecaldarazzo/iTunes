import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        durata=self._view._txtInDurata.value
        durataInt=int(durata)
        self._view.txt_result.controls.clear()
        if durataInt==None:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un tempo in minuti",color="red"))
        elif not isinstance(durataInt,int):
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero!", color="red"))
        else:
            self._model.buildGraph(durataInt)
            self._view.txt_result.controls.append(ft.Text(f"Grafo creato!"))
            self._view.txt_result.controls.append(ft.Text(f"# Nodi: {self._model.getNumNodes()}"))
            self._view.txt_result.controls.append(ft.Text(f"# Archi: {self._model.getNumEdges()}"))
            self._view._ddAlbum.disabled=False
            self.fillDDAlbum()
            self._view._btnAnalisiComp.disabled = False
        self._view.update_page()


    def handleAnalisiComp(self, e):
        album = self._view._ddAlbum.value
        self._view.txt_result.controls.clear()
        durata, dimComp = self._model.getCompConn(album)
        self._view.txt_result.controls.append(ft.Text(f"Componente connessa - {album}"))
        self._view.txt_result.controls.append(ft.Text(f"Dimensione componente = {dimComp}"))
        self._view.txt_result.controls.append(ft.Text(f"Durata componente = {durata}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        durataTot = self._view._txtInSoglia.value
        album = self._view._ddAlbum.value
        durataTotInt = int(durataTot)
        self._view.txt_result.controls.clear()
        if durataTotInt == None:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un tempo in minuti", color="red"))
        elif not isinstance(durataTotInt, int):
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero!", color="red"))
        else:
            setAlbum=self._model.getSetAlbum(durataTotInt,album)
            if setAlbum==[]:
                self._view.txt_result.controls.append(ft.Text(f"Non esiste nessun set di album con durata inferiore a quella inserita"))
            else:
                self._view.txt_result.controls.append(ft.Text(f"Il set di album è composto da:"))
                for a in setAlbum:
                    self._view.txt_result.controls.append(ft.Text(a))
        self._view.update_page()

    def fillDDAlbum(self):
        album=self._model.getNodes()
        for a in album:
            self._view._ddAlbum.options.append(ft.dropdown.Option(a))
        self._view.update_page()