
class Editor:
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
        tablas=["area","carrera","escolaridad","estado_civil","grado_avance","habilidad","idioma"]
        titulos=["Area","Carrera","Escolaridad","Estado Civil","Grado de Avance","Habilidad","Idioma"]

        try:
            c=tablas.index(tabla)
            return titulos[c]
        except Exception:
            return None
        
    def titleToTabla(self,titulo):
        tablas=["area","carrera","escolaridad","estado_civil","grado_avance","habilidad","idioma"]
        titulos=["Area","Carrera","Escolaridad","Estado Civil","Grado de Avance","Habilidad","Idioma"]

        try:
            c=titulos.index(titulo)
            return tablas[c]
        except Exception:
            return None
    
    def tablaId(self,nombre_tabla):
        tablas=["area","carrera","escolaridad","estado_civil","grado_avance","habilidad","idioma"]
        ids=["idArea","idCarrera","idEscolaridad","idEstadoCivil","idGradoAvance","idHabilidad","idIdioma"]

        try:
            c=tablas.index(nombre_tabla)
            return ids[c]
        except Exception:
            return None
        