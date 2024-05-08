from conexion import Conexion
from editor_texto import Editor

reiniciar_campos=False

class Admin():
    columnas=9
    tablas=15
    database="rh3"
    def __init__(self):
        self.cx=Conexion(self.database,self.columnas,self.tablas)
        self.editor=Editor()

    def execute(self,query):
        resu=self.cx.execute_query(query)
        return resu
    
    def getResult(self):
        return self.cx.getFetch()
    
    def close(self):
        self.cx.close()

    def tablaPlural(self,tabla):
        # tabla + "registradas"
        titulos=["Area","Carrera","Escolaridad","Estado Civil","Grado de Avance","Habilidad","Idioma"]

        palabras=tabla.split(" ")
        tabla2=""

        for palabra in palabras:
            tabla2+=palabra
            tabla2+=self.editor.addPlural(palabra)
            
            if(len(palabras)!=1):
                tabla2+=" "

        return tabla2, self.editor.isMale(tabla)
        # if tabla=="Escolaridad" or tabla=="Estado Civil" or tabla=="Habilidad":
        #     print("s")
        # elif tabla=="Grado de Avance":
        #     print(2)
        # else:
        #     return tabla+"s"
# ad=Admin()