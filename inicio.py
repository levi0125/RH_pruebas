from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from sql_admin import Admin

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/catalogos:<string:tabla>')
def area(tabla): 
    conexion=Admin()

    tablas=["area","carrera","escolaridad","estado_civil","grado_avance","habilidad","idioma"]
    ids=["idArea","idCarrera","idEscolaridad","idEstadoCivil","idGradoAvance","idHabilidad","idIdioma"]
    titulos=["Area","Carrera","Escolaridad","Estado Civil","Grado de Avance","Habilidad","Idioma"]
    
    try:
        c=tablas.index(tabla)
    except Exception:
        print("ERROR, NO ESTÁ")
        return redirect("/")
    
    conexion.execute(f"select * from {tabla} order by {ids[c]}")
    datos = conexion.getResult()

    plural,male=conexion.tablaPlural(titulos[c])
    plural=plural.upper()

    # print("\n\n\n",datos)
    # print("\n\n\n",plural)
    return render_template("area.html", comentarios = datos,titulo=titulos[c],tabla_plural=plural,male=male)

@app.route('/area_editar/<string:id>')
def area_editar(id):
    conexion=Admin()
    
    conexion.execute('select idArea, descripcion from area where idArea = %s'%(id))
    dato  = conexion.getResult()

    return render_template("area_edi.html", comentar=dato[0])

@app.route('/area_fedita/<string:id>',methods=['POST'])
def area_fedita(id):
    if request.method == 'POST':
        desc=request.form['descripcion']
        
        conexion=Admin()
        
        conexion.execute('update area set descripcion=%s where idArea=%s'%(desc,id))
        
    return redirect(url_for('area'))

@app.route('/area_borrar/<string:id>')
def area_borrar(id):
    
    conexion=Admin()
    
    conexion.execute('delete from area where idArea = {0}'.format(id))
    
    return redirect(url_for('area'))

@app.route('/area_agregar')
def area_agregar():
    return render_template("area_agr.html")

@app.route('/area_fagrega', methods=['POST'])
def area_fagrega():
    if request.method == 'POST':
        desc = request.form['descripcion']
        
        conexion=Admin()
        
        conexion.execute('insert into area (descripcion) values (%s)'%(desc))
        
    return redirect(url_for('area'))



@app.route('/puesto')
def puesto():
    
    conexion=Admin()


    conexion.execute('select idPuesto, nomPuesto from puesto order by idPuesto')
    datos = conexion.getResult()

    return render_template("puesto.html", pue = datos, dat='   ', catArea = '   ', catEdoCivil = '   ', catEscolaridad = '   ',
                           catGradoAvance = '    ', catCarrera = '    ', catIdioma = ' ', catHabilidad = ' ')


@app.route('/puesto_fdetalle/<string:idP>', methods=['GET'])
def puesto_fdetalle(idP):
    
    conexion=Admin()


    conexion.execute('select idPuesto, nomPuesto from puesto order by idPuesto')
    datos = conexion.getResult()

    conexion.execute(f"""select idPuesto,codPuesto,idArea,nomPuesto,puestoJefeSup,jornada,remunMensual,prestaciones,descripcionGeneral,
            funciones,edad,sexo,idEstadoCivil,idEscolaridad,idGradoAvance,idCarrera,experiencia,conocimientos,manejoEquipo,'
            'reqFisicos,reqPsicologicos,responsabilidades,condicionesTrabajo from puesto where idPuesto = {idP}""" )
    dato = conexion.getResult()

    conexion.execute('select a.idArea, a.descripcion from area a, puesto b where a.idArea = b.idArea and b.idPuesto = %s'%(idP))
    datos1 = conexion.getResult()

    conexion.execute('select a.idEstadoCivil, a.descripcion from estado_civil a, puesto b where a.idEstadoCivil = b.idEstadoCivil and b.idPuesto = %s'%(idP))
    datos2 = conexion.getResult()

    conexion.execute('select a.idEscolaridad, a.descripcion from escolaridad a, puesto b where a.idEscolaridad = b.idEscolaridad and b.idPuesto = %s'%(idP))
    datos3 = conexion.getResult()

    conexion.execute('select a.idGradoAvance, a.descripcion from grado_avance a, puesto b where a.idGradoAvance = b.idGradoAvance and b.idPuesto = %s'%(idP))
    datos4 = conexion.getResult()

    conexion.execute('select a.idCarrera, a.descripcion from carrera a, puesto b where a.idCarrera = b.idCarrera and b.idPuesto = %s'%(idP))
    datos5 = conexion.getResult()

    conexion.execute('select a.idPuesto, b.idIdioma, b.descripcion from puesto a, idioma b, puesto_has_idioma c '
                   'where a.idPuesto = c.idPuesto and b.idIdioma = c.idIdioma and a.idPuesto = %s'%(idP))
    datos6 = conexion.getResult()

    conexion.execute(f'select a.idPuesto, b.idHabilidad, b.descripcion from puesto a, habilidad b, puesto_has_habilidad c where a.idPuesto = c.idPuesto and b.idHabilidad = c.idHabilidad and a.idPuesto = {idP}')
    datos7 = conexion.getResult()
    return render_template("puesto.html", pue = datos, dat=dato[0], catArea=datos1[0], catEdoCivil=datos2[0], catEscolaridad=datos3[0],
                           catGradoAvance=datos4[0], catCarrera=datos5[0], catIdioma=datos6, catHabilidad=datos7)

@app.route('/puesto_borrar/<string:idP>')
def puesto_borrar(idP):
    
    conexion=Admin()
    
    conexion.execute('delete from puesto where idPuesto = %s'%(idP))
    
    conexion.execute('delete from puesto_has_habilidad where idPuesto =%s '%(idP))
    
    conexion.execute('delete from puesto_has_idioma where idPuesto =%s '%(idP))
    
    return redirect(url_for('puesto'))


@app.route('/puesto_agrOp2')
def puesto_agrOp2():
    
    conexion=Admin()
    
    conexion.execute('select idArea, descripcion from area ')
    datos1 = conexion.getResult()

    conexion.execute('select idEstadoCivil, descripcion from estado_civil ')
    datos2 = conexion.getResult()

    conexion.execute('select idEscolaridad, descripcion from escolaridad ')
    datos3 = conexion.getResult()

    conexion.execute('select idGradoAvance, descripcion from grado_avance ')
    datos4 = conexion.getResult()

    conexion.execute('select idCarrera, descripcion from carrera ')
    datos5 = conexion.getResult()

    conexion.execute('select idIdioma, descripcion from idioma ')
    datos6 = conexion.getResult()

    conexion.execute('select idHabilidad, descripcion from habilidad ')
    datos7 = conexion.getResult()

    return render_template("puesto_agrOp2.html", catArea=datos1, catEdoCivil=datos2, catEscolaridad=datos3,
                           catGradoAvance=datos4, catCarrera=datos5, catIdioma=datos6, catHabilidad=datos7)


@app.route('/puesto_fagrega2', methods=['POST'])
def puesto_fagrega():
    if request.method == 'POST':

        if  'idArea' in request.form:
            idAr = request.form['idArea']
        else:
            idAr = '1'
        if 'idEstadoCivil' in request.form:
            idEC = request.form['idEstadoCivil']
        else:
            idEC = '1'
        if 'idEscolaridad' in request.form:
            idEs = request.form['idEscolaridad']
        else:
            idEs = '1'
        if 'idGradoAvance' in request.form:
            idGA = request.form['idGradoAvance']
        else:
            idGA = '1'
        if 'idCarrera' in request.form:
            idCa = request.form['idCarrera']
        else:
            idCa = '1'
        if 'sexo' in request.form:
            sex = request.form['sexo']
        else:
            sex = '1'
        codP = request.form['codPuesto']
        nomP = request.form['nomPuesto']
        pueJ = request.form['puestoJefeSup']
        jorn = request.form['jornada']
        remu = request.form['remunMensual']
        pres = request.form['prestaciones']
        desc = request.form['descripcionGeneral']
        func = request.form['funciones']
        eda = request.form['edad']
        expe = request.form['experiencia']
        cono = request.form['conocimientos']
        manE = request.form['manejoEquipo']
        reqF = request.form['reqFisicos']
        reqP = request.form['reqPsicologicos']
        resp = request.form['responsabilidades']
        conT = request.form['condicionesTrabajo']


    
    conexion=Admin()
    
    conexion.execute(
    """insert into puesto (codPuesto,idArea,nomPuesto,puestoJefeSup,jornada,remunMensual,prestaciones,descripcionGeneral,
    funciones,edad,sexo,idEstadoCivil,idEscolaridad,idGradoAvance,idCarrera,experiencia,conocimientos,manejoEquipo,
    reqFisicos,reqPsicologicos,responsabilidades,condicionesTrabajo) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""%
    (codP, idAr, nomP, pueJ, jorn, remu, pres, desc, func, eda, sex, idEC, idEs, idGA, idCa, expe, cono, manE, reqF,
     reqP, resp, conT))
    

    conexion.execute('select idPuesto from puesto where idPuesto=(select max(idPuesto) from puesto) ')
    dato = conexion.getResult()
    idpue = dato[0]
    idP = idpue[0]

    conexion.execute('select count(*) from idioma ')
    dato = conexion.getResult()
    nidio = dato[0]
    ni = nidio[0] + 1

    for i in range(1, ni):
        idio = 'i' + str(i)
        if idio in request.form:
            conexion.execute('insert into puesto_has_idioma(idPuesto,idIdioma) values (%s,%s)'%(idP, i))
            

    conexion.execute('select count(*) from habilidad ')
    dato = conexion.getResult()
    nhab = dato[0]
    nh =nhab[0]+1

    for i in range(1,nh):
        habi = 'h' + str(i)
        if habi in request.form:
            conexion.execute('insert into puesto_has_habilidad(idPuesto,idHabilidad) values (%s,%s)'%(idP,i))
            

    return redirect(url_for('puesto'))



@app.route('/puesto_editar/<string:idP>')
def puesto_editar(idP):
    
    conexion=Admin()


    conexion.execute('select idPuesto,codPuesto,idArea,nomPuesto,puestoJefeSup,jornada,remunMensual,prestaciones,descripcionGeneral,'
        'funciones,edad,sexo,idEstadoCivil,idEscolaridad,idGradoAvance,idCarrera,experiencia,conocimientos,manejoEquipo,'
        'reqFisicos,reqPsicologicos,responsabilidades,condicionesTrabajo from puesto where idPuesto = %s'%(idP))
    dato = conexion.getResult()

    conexion.execute('select idArea, descripcion from area ')
    datos1 = conexion.getResult()

    conexion.execute('select idEstadoCivil, descripcion from estado_civil ')
    datos2 = conexion.getResult()

    conexion.execute('select idEscolaridad, descripcion from escolaridad ')
    datos3 = conexion.getResult()

    conexion.execute('select idGradoAvance, descripcion from grado_avance ')
    datos4 = conexion.getResult()

    conexion.execute('select idCarrera, descripcion from carrera ')
    datos5 = conexion.getResult()

    conexion.execute('select idIdioma, descripcion from idioma ')
    datos6 = conexion.getResult()

    conexion.execute('select idHabilidad, descripcion from habilidad ')
    datos7 = conexion.getResult()

    conexion.execute('select a.idArea, a.descripcion from area a, puesto b where a.idArea = b.idArea and b.idPuesto = %s'%(idP))
    datos11 = conexion.getResult()

    conexion.execute('select a.idEstadoCivil, a.descripcion from estado_civil a, puesto b where a.idEstadoCivil = b.idEstadoCivil and b.idPuesto = %s'%(idP))
    datos12 = conexion.getResult()

    conexion.execute('select a.idEscolaridad, a.descripcion from escolaridad a, puesto b where a.idEscolaridad = b.idEscolaridad and b.idPuesto = %s'%(idP))
    datos13 = conexion.getResult()

    conexion.execute('select a.idGradoAvance, a.descripcion from grado_avance a, puesto b where a.idGradoAvance = b.idGradoAvance and b.idPuesto = %s'%(idP))
    datos14 = conexion.getResult()

    conexion.execute('select a.idCarrera, a.descripcion from carrera a, puesto b where a.idCarrera = b.idCarrera and b.idPuesto = %s'%(idP))
    datos15 = conexion.getResult()

    conexion.execute('select a.idPuesto, b.idIdioma, b.descripcion from puesto a, idioma b, puesto_has_idioma c '
                   'where a.idPuesto = c.idPuesto and b.idIdioma = c.idIdioma and a.idPuesto = %s'%(idP))
    datos16 = conexion.getResult()

    conexion.execute('select a.idPuesto, b.idHabilidad, b.descripcion from puesto a, habilidad b, puesto_has_habilidad c '
                   'where a.idPuesto = c.idPuesto and b.idHabilidad = c.idHabilidad and a.idPuesto = %s'%(idP))
    datos17 = conexion.getResult()


    return render_template("puesto_edi.html", dat=dato[0], catArea=datos1, catEdoCivil=datos2, catEscolaridad=datos3,
                           catGradoAvance=datos4, catCarrera=datos5, catIdioma=datos6, catHabilidad=datos7,
                           Area=datos11[0], EdoCivil=datos12[0], Escolaridad=datos13[0], GradoAvance=datos14[0],
                           Carrera=datos15[0], Idioma=datos16, Habilidad=datos17)


@app.route('/puesto_fedita/<string:idP>', methods=['POST'])
def puesto_fedita(idP):
    if request.method == 'POST':
        codP = request.form['codPuesto']
        idAr = request.form['idArea']
        nomP = request.form['nomPuesto']
        pueJ = request.form['puestoJefeSup']
        jorn = request.form['jornada']
        remu = request.form['remunMensual']
        pres = request.form['prestaciones']
        desc = request.form['descripcionGeneral']
        func = request.form['funciones']
        eda = request.form['edad']
        sex = request.form['sexo']
        idEC = request.form['idEstadoCivil']
        idEs = request.form['idEscolaridad']
        idGA = request.form['idGradoAvance']
        idCa = request.form['idCarrera']
        expe = request.form['experiencia']
        cono = request.form['conocimientos']
        manE = request.form['manejoEquipo']
        reqF = request.form['reqFisicos']
        reqP = request.form['reqPsicologicos']
        resp = request.form['responsabilidades']
        conT = request.form['condicionesTrabajo']

    
    conexion=Admin()


    conexion.execute("""update puesto set codPuesto = %s, idArea = %s, nomPuesto = %s, puestoJefeSup = %s, jornada = %s,
                  remunMensual = %s, prestaciones = %s, descripcionGeneral = %s, funciones = %s, edad = %s, sexo = %s,
                  idEstadoCivil = %s, idEscolaridad = %s, idGradoAvance = %s, idCarrera = %s, experiencia = %s,
                  conocimientos = %s, manejoEquipo = %s, reqFisicos = %s, reqPsicologicos = %s, responsabilidades = %s,
                  condicionesTrabajo = %s where idPuesto = %s"""%(codP, idAr, nomP, pueJ, jorn, remu, pres, desc, func, eda,
                   sex, idEC, idEs, idGA, idCa, expe, cono, manE, reqF, reqP, resp, conT, idP))
    

    conexion.execute('delete from puesto_has_habilidad where idPuesto =%s '%(idP))
    
    conexion.execute('delete from puesto_has_idioma where idPuesto =%s '%(idP))
    

    conexion.execute('select count(*) from idioma ')
    dato = conexion.getResult()
    nidio = dato[0]
    ni = nidio[0] + 1

    for i in range(1, ni):
        idio = 'i' + str(i)
        if idio in request.form:
            conexion.execute('insert into puesto_has_idioma(idPuesto,idIdioma) values (%s,%s)'%(idP, i))
            

    conexion.execute('select count(*) from habilidad ')
    dato = conexion.getResult()
    nhab = dato[0]
    nh = nhab[0] + 1

    for i in range(1, nh):
        habi = 'h' + str(i)
        if habi in request.form:
            conexion.execute('insert into puesto_has_habilidad(idPuesto,idHabilidad) values (%s,%s)'%(idP, i))
            
    return redirect(url_for('puesto'))




if __name__ == "__main__":
    app.run(debug=True)
