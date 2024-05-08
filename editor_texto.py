
class Editor:
    def __init__(self):
        self.tablas=self.getTables()
        self.titulos=self.getTableTitles()
        self.ids=self.getIds()

    def getIds(self):
        return ["idArea","idCarrera","idEscolaridad","idEstadoCivil","idGradoAvance","idHabilidad","idIdioma"]
    
    def getTables(self):
        return ["area","carrera","escolaridad","estado_civil","grado_avance","habilidad","idioma"]
    
    def getTableTitles(self):
        return ["Area","Carrera","Escolaridad","Estado Civil","Grado de Avance","Habilidad","Idioma"]
    
    def isVowel(self,letra):
        vocales=["a","e","i","o","u"]
        try:
            vocales.index( letra )
            return True
        except Exception:
            return False
    
    def endsVowel(self,word):
        return self.isVowel(word[len(word)-1])
    
    def addPlural(self,palabra):
        if(palabra=="Avance" or palabra =="de"):
            return ""

        if(self.endsVowel(palabra)):
            return "s"
        
        return "es"
    
    def isMale (self,word):
        # titulos=["Area","Carrera","Escolaridad","Estado Civil","Grado de Avance","Habilidad","Idioma"]
        masculinos=["Idioma","Grado de Avance","Estado Civil"]

        try:
            masculinos.index(word)
            return True
        except Exception:
            return False
        
    def tablaToTitle(self,tabla):
        try:
            c=self.tablas.index(tabla)
            return self.titulos[c]
        except Exception:
            return None
        
    def titleToTabla(self,titulo):
        try:
            c=self.titulos.index(titulo)
            return self.tablas[c]
        except Exception:
            return None
    
    def tablaToId(self,nombre_tabla):
        try:
            c=self.tablas.index(nombre_tabla)
            return self.ids[c]
        except Exception:
            return None
        
    def existenciaTabla(self,tabla):
        tablas=self.getTables()
        try:
            c=tablas.index(tabla)
        except Exception:
            print("ERROR, NO ESTÁ")
            return None
        return True