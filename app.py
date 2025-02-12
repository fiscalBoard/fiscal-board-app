from flask import Flask, render_template,jsonify, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
from helper import logger
import random
import string
import secrets
from document_helper import manejar_post
from db import db, Negocio, Cartelera, Documento  # Importar modelos
from datetime import datetime
import json
from flask_wtf.csrf import CSRFProtect

 
url_ngrok = "https://7b00-190-153-8-17.ngrok-free.app/uploads/"
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Clave secreta aleatoria
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pepe.1983@localhost:3306/NegociosDB'  # Tus credenciales
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Autenticación
url = "https://app.ayrshare.com/api/post"
 
  

  
mail = Mail(app)
UPLOAD_FOLDER = '/var/www/html/uploads'  # Carpeta donde se guardarán las imágenes
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Deshabilitar CSRF
app.config['WTF_CSRF_ENABLED'] = True  # Esta línea está bien, ya no necesitas CSRFProtect
csrf = CSRFProtect(app)  # Esta línea se puede comentar o eliminar
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
       

@app.route('/divisas', methods=['GET'])
def divisas():
     
    # URL para los juegos de MLB desde la fecha actual
    api_url = 'https://ve.dolarapi.com/v1/dolares'
    response = requests.get(api_url)
    
    # Verificar si la respuesta fue exitosa
    if response.status_code != 200:
        return "Error al obtener los datos de MLB", response.status_code

    data = response.json()

    # Verificar si hay datos en la respuesta
    oficial_data = [item for item in data if item['fuente'] == 'oficial'] 

    if not oficial_data:
        return "No hay datos en la respuesta del API.", 404

    oficial_data = oficial_data[0]

    return jsonify({'success': True, 'cotizacion': oficial_data}), 200

    
@app.route('/get_negocio', methods=['GET'])
def get_negocio():
    usuario = request.args.get('usuario')
    # Verificar si el usuario está autenticado
    if usuario:
        # Obtener el negocio del usuario logueado
        negocio = Negocio.query.filter_by(usuario=usuario).first()
        
        if negocio:
            logger.info(f"Negocio: {negocio}")
            negocio_serializado = {
                'id': negocio.id,
                'rif': negocio.rif,
                'nombre': negocio.nombre,
                'direccion': negocio.direccion,
                'telefono': negocio.telefono,
                'correo': negocio.correo,
                'fecha_creacion': negocio.fecha_creacion.isoformat(),  # Convertir a formato ISO
                'tipo_negocio': negocio.tipo_negocio,
                'estado': negocio.estado
            }
            return jsonify({'success': True, 'negocio': negocio_serializado}), 200
        else:
            return jsonify({'success': False, 'message': "Negocio no encontrado."}), 404
    else:
        flash('Debes iniciar sesión para acceder a esta página.', 'warning')
        return jsonify({'success': False, 'message': "Se requieren parámetros."}), 403

@app.route('/cartelera_por_usuario', methods=['GET'])
def cartelera_por_usuario():
    usuario = request.args.get('usuario')
    # Verificar si el usuario está autenticado
    if usuario:
        # Obtener el negocio del usuario logueado
        negocio = Negocio.query.filter_by(usuario=usuario).first()
        
        if negocio:
            # Obtener carteleras del negocio actual
            carteleras = Cartelera.query.filter_by(negocio_id=negocio.id).all()
            
            # Crear un diccionario para almacenar los tipos de documento por cartelera
            documentos_por_cartelera = {}
            
            for cartelera in carteleras:
                # Obtener los documentos asociados a la cartelera
                documentos = Documento.query.filter_by(id_cartelera=cartelera.id).all()
                # Usar un conjunto para evitar duplicados
                tipos_documento = set(doc.tipo_documento for doc in documentos)
                documentos_por_cartelera[cartelera.id] = list(tipos_documento)

            logger.info(f"Documentos por cartelera: {documentos_por_cartelera}")
             # Convertir las carteleras a un formato serializable
            carteleras_serializadas = [
                {
                    'id': cartelera.id,
                    'titulo': cartelera.titulo,
                    'descripcion': cartelera.descripcion,
                    'fecha_publicacion': cartelera.fecha_publicacion.isoformat(),  # Convertir a formato ISO
                    'negocio_id': cartelera.negocio_id,  # Incluye el ID del negocio
                    'documentos': documentos_por_cartelera[cartelera.id]  # Agregar los tipos de documentos
                }
                for cartelera in carteleras
            ]
            return jsonify({'success': True, 'carteleras': carteleras_serializadas}), 200
        else:
            return jsonify({'success': False, 'message': "Negocio no encontrado."}), 404
    else:
        flash('Debes iniciar sesión para acceder a esta página.', 'warning')
        return jsonify({'success': False, 'message': "Se requieren parámetros."}), 403
    
@app.route('/')
def home():
    if 'user_id' in session:
        # Obtener el negocio del usuario logueado
        negocio = Negocio.query.get(session.get('user_id'))
        
        # Obtener carteleras del negocio actual
        carteleras = Cartelera.query.filter_by(negocio_id=negocio.id).all() if negocio else []
        
        # Crear un diccionario para almacenar los tipos de documento por cartelera
        documentos_por_cartelera = {}
        
        for cartelera in carteleras:
            # Obtener los documentos asociados a la cartelera
            documentos = Documento.query.filter_by(id_cartelera=cartelera.id).all()
            # Usar un conjunto para evitar duplicados
            tipos_documento = set(doc.tipo_documento for doc in documentos)
            documentos_por_cartelera[cartelera.id] = list(tipos_documento)  # Convertir a lista si es necesario

        logger.info(f"Documentos por cartelera: {documentos_por_cartelera}")
        return render_template('home.html', anuncios=carteleras, current_user=negocio, documentos=documentos_por_cartelera)
    else:
        flash('Debes iniciar sesión para acceder a esta página.', 'warning')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
     
    """
    Vista para registrar un nuevo negocio.

    Si el método es POST, se toman los campos del formulario y se crea un nuevo objeto Negocio.
    Se realizan validaciones simples: se verifica que todos los campos obligatorios estén completos.
    Si la contraseña existe, se genera un hash con scrypt y se crea el nuevo negocio.
    Se intenta agregar el nuevo negocio a la base de datos y se muestra un mensaje de éxito o error.
    Si el método es GET, se renderiza la plantilla de registro.
    """
    if request.method == 'POST':
        body = json.loads(request.data.decode('utf-8'))
        logger.info(f"Intentando registrar un nuevo negocio. {body}")
        rif = body.get('rif')
        nombre_negocio = body['nombre_negocio']
        direccion = body['direccion']
        telefono = body['telefono']
        correo_negocio = body['correo_negocio']
        tipo_negocio = body['tipo_negocio']
        usuario = body['usuario']
        password = body['password']

        # Validaciones simples
        if not rif or not nombre_negocio or not direccion or not usuario or not password:
            flash('Por favor, completa todos los campos obligatorios.', 'danger')
            return jsonify({'success': False, 'message': "Por favor, completa todos los campos obligatorios."}), 401
            #return render_template('register.html')

        if password:  # Solo genera el hash si la contraseña existe
            hashed_password = generate_password_hash(password, method='scrypt')

            nuevo_negocio = Negocio(
                rif=rif,
                nombre=nombre_negocio,
                direccion=direccion,
                telefono=telefono,
                correo=correo_negocio,
                fecha_creacion=datetime.now(),
                tipo_negocio=tipo_negocio,
                usuario=usuario,
                password=hashed_password
            )

            try:
                db.session.add(nuevo_negocio)
                db.session.commit()
                flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
                #return redirect(url_for('login'))
                return jsonify({'success': True, 'message': 'Registro exitoso. Ahora puedes iniciar sesión '})
            except Exception as e:
                db.session.rollback()  # Deshacer cambios en caso de error
                logger.info(f"Error al registrar el usuario: {e}")
                flash('Error al registrar el negocio. Por favor, inténtalo de nuevo.', 'danger')
                return jsonify({'success': False, 'message': e}), 403
                #return render_template('register.html', error=str(e))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        body = json.loads(request.data.decode('utf-8'))
        usuario = body['usuario']
        password = body['password']
        logger.info(f"Usuario: {usuario} // Contraseña: {password}")
        negocio = Negocio.query.filter_by(usuario=usuario).first()
        if negocio and check_password_hash(negocio.password, password):
            logger.info(f"Usuario: {negocio.usuario} // Contraseña: {password}")            
            session['user_id'] = negocio.id
            session['usuario'] = negocio.usuario
            
            session['negocio'] = {
                'id': negocio.id,
                'rif': negocio.rif,
                'nombre': negocio.nombre,
                'direccion': negocio.direccion,
                'telefono': negocio.telefono,
                'correo': negocio.correo,
                'tipo_negocio': negocio.tipo_negocio,
                'estado': negocio.estado
            }

            flash('Inicio de sesión exitoso.', 'success')
             
            return jsonify({'success': True, 'message': 'Inicio de sesión exitoso.'})        
            #return redirect(url_for('home'))
        flash('Credenciales incorrectas. Intenta de nuevo.', 'danger')
        #return jsonify({'success': False, 'message': 'Credenciales incorrectas.'}), 401
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    #return redirect(url_for('login'))
    return jsonify({'success': True, 'message': 'Cerrar Sesion exitoso.'})

@app.route('/cartelera', methods=['GET', 'POST'])
def crear_cartelera():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        body = json.loads(request.data.decode('utf-8'))
        titulo = body['titulo']
        descripcion = body['descripcion']
        #fecha_vigencia = request.form['fecha_vigencia']
        #tipo_anuncio = request.form['tipo_anuncio']
        usuario_id = session.get('user_id') 
        # Manejar la subida de la imagen

        nuevo_anuncio = Cartelera(
            titulo=titulo,
            descripcion= descripcion,           
            negocio_id=usuario_id  # Asocia el anuncio con el negocio del usuario logueado
        )
        
           
        db.session.add(nuevo_anuncio)
        db.session.commit()
        logger.info('Cartelera creada con éxito!', 'success')
        flash('Cartelera creada con éxito!', 'success')
        return jsonify({'success': True, 'message': 'Cartelera creada con éxito'})#redirect(url_for('home'))

    return render_template('crear_cartelera.html' , current_user=session.get('negocio'))


@app.route('/crear_documento<int:id>', methods=['GET', 'POST'])
def crear_documento(id):
    if not session.get('user_id'):
        logger.info("No hay usuario logueado")
        return redirect(url_for('login'))

    logger.info(f"METODOS: {request.method}")

    if request.method == 'POST':
        return manejar_post(id, app)

    documentos = Documento.query.filter_by(id_cartelera=id).all()
    current_user = session.get('negocio')
    return render_template('crear_documento.html', id=id, documentos=documentos, current_user=current_user)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            msg = Message('Nueva contraseña', recipients=[email])
            msg.body = f'Tu nueva contraseña es: {new_password}'
            mail.send(msg)
            flash('Se ha enviado una nueva contraseña a tu correo.', 'success')
        else:
            flash('El correo no está registrado.', 'danger')
    return render_template('forgot_password.html')
@app.route('/eliminar_cartelera/<int:id>', methods=['POST'])
def eliminar_cartelera(id):
    if not session.get('user_id'):
        flash('Debes iniciar sesión para eliminar una cartelera.', 'danger')
        return redirect(url_for('login'))

    cartelera = Cartelera.query.get(id)
    
    if cartelera is None:
        flash('La cartelera no existe.', 'danger')
        return redirect(url_for('home'))

    try:
        db.session.delete(cartelera)
        db.session.commit()
        flash('Cartelera eliminada con éxito.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la cartelera. Por favor, inténtalo de nuevo.', 'danger')
        logger.info(f"Error al eliminar la cartelera con ID: {id}. Detalle del error: {e}")

    return redirect(url_for('home'))

@app.route('/eliminar_anuncio<int:id>?<int:cartelera>', methods=['POST'])
def eliminar_anuncio(id, cartelera):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    logger.info(f"Intentando eliminar el anuncio con ID: {id}")  # Imprimir el ID del anuncio a eliminar
    documento = Documento.query.get(id)
    
    if documento is None:
        flash('La cartelera no existe.', 'danger')
        logger.info('La cartelera no existe.', 'danger')
        return redirect(url_for('home'))
    logger.info(f"Documento con ID: {documento} no encontrado.")
    try:
        db.session.delete(documento)  # Eliminar la cartelera encontrada
        db.session.commit()
        flash('Documento eliminada con éxito.', 'success')
        logger.info(f"Documento con ID: {id} eliminada.")  # Confirmación de eliminación
    except Exception as e:
        db.session.rollback()  # Deshacer cambios en caso de error
        flash('Error al eliminar la documento. Por favor, inténtalo de nuevo.', 'danger')
        logger.info(f"Error al eliminar la documento con ID: {id}. Detalle del error: {e}")
    documentos = Documento.query.filter_by(id_cartelera=cartelera).all()    
    return render_template('crear_documento.html', id=cartelera, documentos=documentos, current_user=session.get('negocio'))

@app.route('/eliminar_varios_anuncios', methods=['POST'])
def eliminar_varios_anuncios():
    anuncios_ids = request.form.getlist('anuncios')  # Obtener los IDs de los anuncios seleccionados
    logger.info(f"IDs de anuncios seleccionados para eliminar: {anuncios_ids}")  # Imprimir los IDs seleccionados
    if anuncios_ids:
        for id in anuncios_ids:
            anuncio = Cartelera.query.get(id)
            if anuncio:
                db.session.delete(anuncio)
                logger.info(f"Anuncio con ID: {id} eliminado.")  # Confirmación de eliminación
            else:
                logger.info(f"Anuncio con ID: {id} no encontrado.")  # Mensaje de error para anuncios no encontrados
        db.session.commit()
        flash('Anuncios eliminados con éxito.', 'success')
    else:
        flash('No se han seleccionado anuncios para eliminar.', 'warning')
        logger.info("No se han seleccionado anuncios para eliminar.")  # Mensaje de advertencia
    return redirect(url_for('home'))

@app.route('/editar_cartelera<int:id>', methods=['GET', 'POST'])
def editar_cartelera(id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    anuncio = Cartelera.query.get(id)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        anuncio.titulo = request.form['titulo']
        anuncio.descripcion = request.form['descripcion']
        anuncio.fecha_publicacion = datetime.now()
        #anuncio.fecha_vigencia = request.form['fecha_vigencia']
        #anuncio.tipo_anuncio = request.form['tipo_anuncio']
        
        # Guardar cambios en la base de datos
        db.session.commit()
        flash('Anuncio actualizado con éxito.', 'success')
        #return redirect(url_for('home'))
        return jsonify({'success': True, 'message': 'Cartelera editada exitosamente.'})
    current_user = None
    if session['negocio']:
        current_user = session['negocio']
    
    return render_template('editar_cartelera.html', anuncio=anuncio, current_user=current_user)
@app.route('/imagenes_anuncios<int:cartelera_id>')
def imagenes_anuncios(cartelera_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    # Supongamos que tienes una función para obtener los anuncios del usuario actual
    cartelera = Cartelera.query.get(cartelera_id)
    documentos = Documento.query.filter_by(id_cartelera=cartelera_id).all()  
        # Ajusta según tu modelo de usuario y anuncios
    # Obtener el negocio asociado al primer anuncio (suponiendo que todos pertenecen al mismo negocio)
    negocio = Negocio.query.filter_by(id=session['user_id']).first()
    logger.info(f"Negocio: {negocio} // Documentos: {documentos}")
    return render_template('imagenes_anuncios.html',cartelera_id=cartelera_id, anuncios=documentos, negocio=negocio, cartelera=cartelera, current_user=negocio)
    
@app.route('/get_imagenes_anuncios', methods=['GET'])
def get_imagenes_anuncios():
    cartelera_id = request.args.get('cartelera_id')
    if not cartelera_id:
        return jsonify({'success': False, 'documentos': "Algunos datos son requerido"}), 400
    # Supongamos que tienes una función para obtener los anuncios del usuario actual
    # cartelera = Cartelera.query.get(cartelera_id)
    documentos = Documento.query.filter_by(id_cartelera=cartelera_id).all()  
    if documentos:
     # Serializar los documentos
        documentos_serializados = [
            {
                'id': doc.id,
                'id_cartelera': doc.id_cartelera,
                'tipo_documento': doc.tipo_documento,
                'archivo': doc.archivo,
                'fecha_subida': doc.fecha_subida.isoformat()  # Convertir a formato ISO
            }
            for doc in documentos
        ]
        return jsonify({'success': True, 'documentos': documentos_serializados}), 200
    else:
        return jsonify({'success': True, 'documentos': []}), 200
    


@app.route('/uploads/<path:filename>')
def serve_image(filename):
    file = os.path.join(*filename.split('/')[-2:])
    logger.info(f"----- FILE NAME -- {file}-- ")
    directory = '/var/www/html/uploads'
    return send_from_directory(directory, file)
    

@app.route('/eliminar_documentos/<int:id>', methods=['POST'])
def eliminar_documentos(id):
    if not session.get('user_id'):
        flash('Debes iniciar sesión para eliminar documentos.', 'danger')
        return redirect(url_for('login'))

    documentos = Documento.query.filter_by(id_cartelera=id).all()
    
    if not documentos:
        flash('No hay documentos asociados a esta cartelera.', 'warning')
        return redirect(url_for('home'))

    try:
        for documento in documentos:
            db.session.delete(documento)
        db.session.commit()
        flash('Documentos eliminados con éxito.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar documentos. Por favor, inténtalo de nuevo.', 'danger')
        logger.info(f"Error al eliminar documentos de la cartelera con ID: {id}. Detalle del error: {e}")

    return redirect(url_for('home'))
  
if __name__ == '__main__':    
    
    logger.info("Servidor Flask en ejecución...")
    app.run(host='0.0.0.0', debug=True, port=8000, use_reloader=False)