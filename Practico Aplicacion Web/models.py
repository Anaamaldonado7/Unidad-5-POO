from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Curso(db.Model):#Clase que vincula la base de datos y va creando instancias
    __tablename__ = 'curso' #nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)#columna1
    anio = db.Column(db.Integer, nullable=False)#columna2
    division = db.Column(db.Integer, nullable=False)#columna3
    idpreceptor = db.Column(db.Integer, db.ForeignKey('preceptor.id'))#columna4
    cursos_preceptor = db.relationship('Preceptor', backref='curso')#asociacion entre preceptor y curso (1 curso tiene un preceptor)

class Estudiante(db.Model):
    __tablename__='estudiante'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    dni = db.Column(db.String(12), nullable=False)
    idcurso = db.Column(db.Integer, db.ForeignKey('curso.id'))

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(10), nullable=False)
    codigoclase = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso = db.relationship('Curso', backref='asistencias')
    asistio = db.Column(db.String(1), nullable=False)
    justificacion = db.Column(db.String(100), nullable=True)
    idestudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    estudiante = db.relationship('Estudiante', backref='asistencias')   

class Preceptor(db.Model):
    __tablename__='preceptor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    clave = db.Column(db.String(100), nullable=False)
    cursos = db.relationship('Curso', backref='preceptor')