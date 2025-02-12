from flask import Flask, render_template,jsonify, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
from helper import logger
import random
import string
from document_helper import manejar_post
from db import db, Negocio, Cartelera, Documento  # Importar modelos
from datetime import datetime
import json
from flask_wtf.csrf import CSRFProtect

 
url_ngrok = "https://7b00-190-153-8-17.ngrok-free.app/uploads/"
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pepe.1983@localhost:3306/NegociosDB'  # Tus credenciales
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


  
if __name__ == '__main__':    
    
    logger.info("Servidor Flask en ejecución...")
    app.run(host='0.0.0.0', debug=True, port=8000, use_reloader=False)