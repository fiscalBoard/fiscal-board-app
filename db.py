from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Negocio(db.Model):
    __tablename__ = 'Negocios'  # Asegúrate de que el nombre de la tabla coincida con el de la base de datos
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rif = db.Column(db.String(15), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(15), default=None)
    correo = db.Column(db.String(100), default=None)
    fecha_creacion = db.Column(db.Date, default=datetime.utcnow)
    tipo_negocio = db.Column(db.Enum('Comercio', 'Servicio', 'Industria', 'Otro'), nullable=False)
    usuario = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.Enum('Activo', 'Inactivo'), default='Activo')
    
    
    

class Propietario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(15), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    correo = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    negocio_id = db.Column(db.Integer, db.ForeignKey('negocio.id'))
    
class Cartelera(db.Model):
    __tablename__ = 'Carteleras'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=False, default=datetime.utcnow)    
    negocio_id = db.Column(db.Integer, db.ForeignKey('Negocios.id'), nullable=False)  # Clave foránea

    # Definir la relación con el modelo Negocio
    negocio = db.relationship('Negocio', backref='Carteleras')  # Relación inversa
    documentos = db.relationship("Documento", back_populates="cartelera")
    def __repr__(self):
        return f"<Cartelera {self.titulo}>"
    
class Documento(db.Model):
    __tablename__ = 'Documentos'

    id = db.Column(db.Integer, primary_key=True)
    id_cartelera = db.Column(db.Integer, db.ForeignKey('Carteleras.id'), nullable=False)
    tipo_documento = db.Column(db.String(100), nullable=False)
    archivo = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.Date, nullable=False)

    # Relación
    cartelera = db.relationship("Cartelera", back_populates="documentos")