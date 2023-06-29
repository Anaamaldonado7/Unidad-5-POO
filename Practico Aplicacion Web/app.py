from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from string import hexdigits
import hashlib

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db 
from models import Preceptor, Estudiante, Curso, Asistencia

@app.route('/')
def inicio():
	return render_template('ingresoUsuario.html')

@app.route('/verificacion',methods= ['POST','GET'])
def verificacion():
    email=request.form['email']
    clave=request.form['password']
    print(email,clave)
    if not email and not clave:
        return render_template('error.html',error="No se ingresaron datos, intente nuevamente.")
    else:
        password=(hashlib.md5(bytes(clave, encoding='utf-8'))).hexdigest() #metodo para encriptar la contraseña
        exists = db.session.query(db.exists().where(Preceptor.correo == email, Preceptor.clave == password)).scalar() #metodo para verificar si existen los datos en la base de datos
        print(exists)
        if exists == True:
            return redirect(url_for('preceptor',correo = email)) #redirect redirecciona a un metodo
        else:
            return render_template('error.html',error="Credenciales incorrectas, intente nuevamente") #render_template muestra una ventana
            
@app.route('/preceptor',methods =['POST','GET'] ) #metodo para guardar la sesion actual del preceptor y llamar la ventana de opciones
def preceptor():
    correo = request.args.get('correo')
    session["preceptor"] = correo
    return render_template('opcionesPreceptor.html')

@app.route('/registraAsistencia', methods=['GET', 'POST'])  
def registraAsistencia():
    correoPrecep = session.get("preceptor")
    print(correoPrecep)
    preceptor = Preceptor.query.filter_by(correo=correoPrecep).first() #Filtra la base de datos del preceptor segun el correo ingresado y guarda la instancia
    print(preceptor)
    cursos = Curso.query.filter_by(idpreceptor=preceptor.id).all() #Filtra la base de datos de los cursos segun el curso que tiene el preceptor y guarda todas las instancias que le corresponden
    return render_template('registraAsistencia.html',cursos=cursos,preceptor=preceptor)   

@app.route('/asistenciaCurso',methods=['POST','GET'])
def asistenciaCurso():
    idcurso=request.form['cursos']
    curso = Curso.query.filter_by(id=idcurso).first()
    alumnos=Estudiante.query.all()
    return render_template('asistenciaCurso.html', curso=curso, alumnos=alumnos)          

@app.route('/asistenciaAlumnos', methods=['GET'])
def asistenciaAlumnos():
    idcurso = request.args.get('idcurso')
    tipoclase = request.args.get('clase')
    fecha = request.args.get('fecha')
    idalumno = request.args.get('alumno')
    alumno = Estudiante.query.filter_by(id=idalumno).first()
    return render_template('confirmarAsistencia.html', tipoclase=tipoclase, fecha=fecha, alumno=alumno, idcurso=idcurso, idalumno=idalumno)            

@app.route('/confirmarAsistencia', methods=['POST'])
def confirmarAsistencia():
    idcurso = request.args.get('idcurso')
    asistencia = Asistencia(fecha=request.form['fecha'], codigoclase=request.form['tipoclase'], asistio=request.form['asis'], justificacion=request.form['justificacion'], idestudiante=request.form.get('idalumno'))
    db.session.add(asistencia)
    db.session.commit()
    cursos=Curso.query.all()
    return redirect(url_for('registraAsistencia', cursos=cursos))
    
@app.route('/listarAsistencia')
def listarAsistencia():
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    cursos = Curso.query.filter_by(idpreceptor=preceptor.id).all()
    return render_template('seleccionaCurso.html', cursos=cursos, preceptor=preceptor)

@app.route('/informe',methods=['POST','GET'])
def informe():
    idcurso=request.form['cursos']
    curso = Curso.query.filter_by(id=idcurso).first()
    alumnos = Estudiante.query.all()
    asistencia=Asistencia.query.all()
    print(curso)
    print(alumnos)
    print(asistencia)
    return render_template('listarDatos.html', curso=curso, alumnos=alumnos, asistencia=asistencia)           
             
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)