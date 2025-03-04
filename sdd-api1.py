import json
from urllib import response
#aca esta la configuracion de la bd y claves
from config import db, app
from modelo.Usuario import Usuario
from modelo.Vehiculo import Vehiculo
from modelo.Rol import Rol
from modelo.Tarjeton import Tarjeton

from sqlalchemy import false, text
from flask_httpauth import HTTPBasicAuth
import os
import ssl
from flask import request, jsonify, render_template, redirect, url_for,Response, make_response, send_from_directory
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

import hashlib
import uuid
from http import HTTPStatus
from typing import Optional
import re
from functools import wraps
import logging
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
 
api = Api(app)
auth = HTTPBasicAuth()
jwt = JWTManager(app)

'''leemos la configuracion de la aplicacion, donde esta la bd y claves
with open('config.json', 'r') as f:
    config = json.load(f)
	
db = SQLAlchemy(app)'''

#vacio la bd
sql = text("delete from usuarios ")
db.session.execute(sql)
sql = text("delete from roles ")
db.session.execute(sql)
sql = text("delete from tarjetones ")
db.session.execute(sql)
sql = text("delete from vehiculos ")
db.session.execute(sql)
db.session.commit()

#precargamos la BD con datos
for i in range(1, 4):
    hashed_password = generate_password_hash("password"+str(i))
    new_api_key = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    new_user = Usuario(username="user"+str(i), password=hashed_password,idRol = i, api_key = new_api_key)
    db.session.add(new_user)

new_vehiculo = Vehiculo(dominio = 'AG071MT',segmento = 'SEDAN',marca ='TOYOTA',modelo ='Corolla 1.8 XEI L/20 CVT HYBRID',motor ='2ZR2T66831',chasis = '9BRBZ3BE1P4046263',año = '2023')
db.session.add(new_vehiculo)
new_vehiculo = Vehiculo(dominio = 'AG071MW',segmento = 'SEDAN',marca ='TOYOTA',modelo ='Corolla 1.8 XEI L/20 CVT HYBRID',motor ='2ZR2T63812',chasis = '9BRBZ3BE7P4046185',año = '2023')
db.session.add(new_vehiculo)
new_vehiculo = Vehiculo(dominio = 'AG071NF',segmento = 'UTILITARIO',marca ='RENAULT',modelo ='Kangoo II Express Confort 5A 1.6 SCE',motor ='H4MJ759Q238991',chasis = '8A18SRYD4RL703220',año = '2023')
db.session.add(new_vehiculo)
new_vehiculo = Vehiculo(dominio = 'AG071NI',segmento = 'UTILITARIO',marca ='RENAULT',modelo ='Kangoo II Express Confort 5A 1.6 SCE',motor = 'H4MJ759Q231805',chasis = '8A18SRYD4RL680781',año = '2023')
db.session.add(new_vehiculo)

new_rol = Rol(nombreRol = 'Admin')
db.session.add(new_rol)
new_rol = Rol(nombreRol = 'Gestor')
db.session.add(new_rol)
new_rol = Rol(nombreRol = 'Agente')
db.session.add(new_rol)

db.session.commit()

#web services endpoints

#1 ubico los certificados para HTTPS
base_dir = os.path.abspath(os.path.dirname(__file__))
cert_path = os.path.join(base_dir, 'server.crt')
key_path = os.path.join(base_dir, 'server.key')	
assert os.path.exists(cert_path), f"server.crt no encontrado en {cert_path}"
assert os.path.exists(key_path), f"server.key no encontrado en {key_path}"

def create_ssl_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path, password='password1')
    return context

######2

#funcion de verificacion de autenticacion
@auth.verify_password
def verify_password(username, password):
        
    '''if not username or not password:
        return {'message': 'Username and password are required'}, 401
        
    user = Usuario.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return {'message': 'Invalid username or password'}, 401'''
    user = Usuario.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return username

#funcion llamada en caso de error de autenticacion, en caso de error se envia 401
@auth.error_handler
def auth_error(status):
    
    return {'message': 'Usuario invalido'}, status, {'Content-Type': 'text/plain'}

#nota: como estamos haciendo pruebas con front embebido se deshabilito dos controles de headers
@app.after_request
def remove_header(response):
    #para que en las solicitudes de autentication basic no lance el browser el cartel de credenciales
    del response.headers['Www-authenticate']    
    response.headers['Cache-Control'] = 'no-store' 
    #devuelvo datos asi que no se necesita que esten en un objeto html especifico
    response.headers['Content-Security-Policy'] = 'frame-ancestors \'none\''
    response.headers['X-Frame-Options'] = 'DENY'
    #siempre retorno json, LUEGO habilitar cuando la api este sin el front embebido de prueba
    #como estamos haciendo pruebas desde un cliente embebido de prueba en este caso obligo a que si hay un determinado header en la respuesta que devuelva html
    #response.headers['Content-Type'] = 'application/json'
    #siempre solicito que se comuniquen con https
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    #indico al browser que siempre use el tipo de contenido especificado y que no intente averiguarlo, LUEGO habilitar
    #response.headers['X-Content-Type-Options'] = 'nosniff'

    return response

class Login(Resource):
    #funcion a llamar en caso de exito de autenticacion
    @auth.login_required
    def get(self):
        user = auth.current_user()
       # response.headers.set['X-Requested-With'] = 'None'
        #return {'message': 'Usuario logueado'}, 200, {'Content-Type': 'text/plain'}
        return {'message': 'Usuario logueado'}, 200, {'Content-Type': 'text/plain'}

####3
#por default se registran como usuarios con rol Gestor
class Register(Resource):
    def post(self):
        #recibo los datos en el header
        username = request.headers.get('usuario')
        password = request.headers.get('password')

        #sanitizacion de entradas
        if not sanitizacion(LONGMAXINPUT,username):
            return {'message': 'Username debe ser valido y debe tener una longitud valida'}, 400,{'Content-Type': 'application/json'}
        if not sanitizacion(LONGMAXINPUT,password):
            return {'message': 'Password debe ser valido y debe tener una longitud valida'}, 400,{'Content-Type': 'application/json'}
        if not verificarIntervalo(LONGMININPUT, LONGMAXINPUT,password):
            return {'message': 'Password debe ser valido'}, 400,{'Content-Type': 'application/json'}

        #rol = request.headers.get('rol')
        rol = 2

        if not username or not password:
            return {'message': 'Username y password son requeridos'}, 400,{'Content-Type': 'application/json'}
        
        if Usuario.query.filter_by(username=username).first():
            return {'message': 'Username ya existe'}, 400
        
        api_key = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()        
        hashed_password = generate_password_hash(password)
        new_user = Usuario(username=username, password=hashed_password,idRol = rol, api_key=api_key)
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'Usuario registrado exitosamente', 'api_key': api_key}, 201

#obtengo el apikey de un usuario
class GetApiKey(Resource):
    def post(self): 
        #verificar contenttype de las solicitudes
        contentType = request.headers.get('Content-Type')
        if not verificarRequestValido(CONTENT_TYPE_VALIDO,contentType):
            return {'message': 'Tipo de contenido de solicitud invalido'}, 415,{'Content-Type': 'application/json'}
        
        username = request.headers.get('usuario')
        password = request.headers.get('password')
        
        if not username or not password:
            return {'message': 'Usuario y password son requeridos'}, 400

        #sanitizacion de entradas
        if not sanitizacion(LONGMAXINPUT,username):
            return {'message': 'Username debe ser valido y debe tener una longitud valida'}, 400
        if not sanitizacion(LONGMAXINPUT,password):
            return {'message': 'Password debe ser valido y debe tener una longitud valida'}, 400

        user = Usuario.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'User name o password invalidos'}, 401
        
        mi_api_key = user.api_key #hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        user.api_key = mi_api_key
        db.session.commit()
        
        return {'message': 'API key devuelto exitosamente', 'api_key': mi_api_key}, 200

class ProtectedResourceAPIKEY(Resource):
    def get(self):
        api_key = request.headers.get('X-API-KEY')
        #sanitizacion de entradas
        if not sanitizacion(LONGMAXINPUT,api_key):
            return {'message': 'Username debe ser valido y debe tener una longitud valida'}, 400

        if not api_key:
            return {'message': 'API key no recibido'}, 401
        
        user = Usuario.query.filter_by(api_key=api_key).first()
        if not user:
            return {'message': 'API key invalido'}, 403
        
        return {'message': f'Hola, {user.username}'}, 200

####4 JWT
class LoginJWT(Resource):
    def post(self):
        username = request.headers.get('usuario')
        password = request.headers.get('password')

        if not username or not password:
            return {'message': 'Username y password son requeridos'}, 400
        
        user = Usuario.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'Username o password invalido'}, 401
        
        # Creo el objeto de payload que estara en el token
        user = UserObjectJWT(username=username, roles=[user.idRol])
        access_token = create_access_token(user)
        return {'message': 'Usuario logeado','access_token': access_token}, 200

#recurso solo protegido por existencia de u token jwt valido
class ProtectedResourceJWT(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hola, {current_user}'}, 200
###6, es una solicitud con un metodo no permitida, se retorna la respuesta default

###7
#valida solo que los inputs tengan caracteres validos del alfabeto español y _
#y el tamaño del body por defecto tiene un maximo de 2mb
#los tipos de los datos se validan por exception en puntos mas adelante
#se usa el register apikey como ejemplo
patron = re.compile(r"^\w+$")
LONGMININPUT = 8
LONGMAXINPUT = 80
def verificarCaracteres(dato):
    return  patron.match(dato) is not None

def verificarIntervalo(longmin, longmax,dato):
    if len(dato) < longmin:
        return False
    else:
        if len(dato) > longmax:
            return False
    return True

def verificarLongitudMax(longmax,dato):
    if len(dato) > longmax:
        return False
    return True

def sanitizacion(longmax, dato):
    if verificarCaracteres(dato) and verificarLongitudMax(longmax,dato):
        return True
    return False


###8 validacion de headers del tipo de solicitud
CONTENT_TYPE_VALIDO = 'application/json'
def verificarRequestValido(contentType,dato):
    if dato != contentType:
        return False
    return True

###9, existen 3 conjuntos de recursos que son administrados por un conjunto de roles
#datos que seran guardados en el payload del token jwt
class UserObjectJWT:
   def __init__(self, username, roles):
      self.username = username
      self.roles = roles

@jwt.additional_claims_loader
def add_claims_to_access_token(user):
   return {'roles': user.roles}
#funcion llamada en la creacion del token para definir la identidad del token
@jwt.user_identity_loader
def user_identity_lookup(user):
   return user.username


#defino decoradores para verificar que exista el token y que sean del rol adecuado segun el recurso que se protege
ADMIN = 1
GESTOR = 2
AGENTE = 3
def admin_required(fn):
   @wraps(fn)
   def wrapper(*args, **kwargs):
      verify_jwt_in_request()
      claims = get_jwt()
      print(claims['roles'])
      if claims['roles'][0] != ADMIN:
         return {'message': 'Solo Admins'}, 403
      else:
         return fn(*args, **kwargs)
   return wrapper

def gestor_required(fn):
   @wraps(fn)
   def wrapper(*args, **kwargs):
      verify_jwt_in_request()
      claims = get_jwt()
      print(claims['roles'])
      if claims['roles'][0] != GESTOR:
         return {'message': 'Solo Gestores'}, 403
      else:
         return fn(*args, **kwargs)
   return wrapper

def agente_required(fn):
   @wraps(fn)
   def wrapper(*args, **kwargs):
      verify_jwt_in_request()
      claims = get_jwt()
      print(claims['roles'])
      if claims['roles'][0] != AGENTE:
         return {'message': 'Solo Agentes'}, 403
      else:
         return fn(*args, **kwargs)
   return wrapper

class LoginJWTROL(Resource):
    def post(self):
      try:        
        
        #verificar contenttype de las solicitudes
        contentType = request.headers.get('Content-Type')
        if not verificarRequestValido(CONTENT_TYPE_VALIDO,contentType):
            return {'message': 'Tipo de contenido de solicitud invalido'}, 415,{'Content-Type': 'application/json'}
        
        username = request.headers.get('usuario')
        password = request.headers.get('password')
        
        if not username or not password:
            return {'message': 'Usuario y password son requeridos'}, 400

        #sanitizacion de entradas
        if not sanitizacion(LONGMAXINPUT,username):
            return {'message': 'Username debe ser valido y debe tener una longitud valida'}, 400
        if not sanitizacion(LONGMAXINPUT,password):
            return {'message': 'Password debe ser valido y debe tener una longitud valida'}, 400
        
        logger.debug(f"POST request received at /usuarios/loginJWTROL with name: {username}")

        user = Usuario.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            logger.error("Usuario o pass no validos")
            return {'message': 'Username o password invalido'}, 401
        
        # Creo el objeto de payload que estara en el token
        user = UserObjectJWT(username=username, roles=[user.idRol])
        access_token = create_access_token(user)
        logger.debug(f"Usuario logueado: {username}")

        return {'message': 'Usuario logeadojwtrol','access_token': access_token}, 200
      except:
          logger.error("ERROR received at /usuarios/loginJWTROL")
          return {'message': 'Momentaneamente no disponible'}, 500
#recurso protegido por jwt y rol admin
class ProtectedResourceJWTAdmin(Resource):
    @admin_required
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hola, {current_user}'}, 200  
#recurso protegido por jwt y rol gestor
class ProtectedResourceJWTGestor(Resource):
    @gestor_required
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hola, {current_user}'}, 200  
#recurso protegido por jwt y rol agente
class ProtectedResourceJWTAgente(Resource):
    @agente_required
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hola, {current_user}'}, 200  


###10 manejo de errores
# siempre los endpoints devolveran errores genericos salvo en casos especiales de regitro de nuevos usuarios
#toda funcion tendra un try catch
class ErrorEmitido(Resource):
    def post(self):
      try:        
        raise Exception("Sorry, no numbers below zero")
      except:
          return {'message': 'Momentaneamente no disponible'}, 500



###11 logs para auditoria
#siempre los parametros enviados al log estan sanitizados con verificarCaracteres(dato)
# Configurar el logging
logging.basicConfig(
    filename='D:\\logVehiculos.log',  # Cambia la ruta según tu entorno
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
logger = logging.getLogger(__name__)


###12 headers seguros
#esta funcion no se usa , se agregan los headers en una funcion de after_request de mas arriba
def headersSeguros():
   #para no cachear la respuesta
   h1 = "'Cache-Control': 'no-store'"
   #devuelvo datos asi que no se necesita que esten en un objeto html especifico
   h2 = "'Content-Security-Policy': 'frame-ancestors none'"
   h3 = "'X-Frame-Options': 'DENY'"
   #siempre retorno json
   h4 = "'Content-Type':'application/json'"
   #siempre solicito que se comuniquen con https
   h5 = "'Strict-Transport-Security':'max-age=31536000; includeSubDomains; preload'"
   #indico al browser que siempre use el tipo de contenido especificado y que no intente averiguarlo
   h6 = "'X-Content-Type-Options': 'nosniff'"
   return h1+","+h2+","+h3+","+h4+","+h5+","+h6


###13 CORS
#CORS(app) habilito cors para todos los endpoints
#habilito cors solo para determinados endpoints poniendo el decorador adecuado
#en caso de necesitar aplicarlo solo a determinados endpoints agregarlo con el decorator especifico de cors @cross_origin(origins='localhost:5000') sobre el endpoint
CORS(app, resources={r"/v1/*": {"origins": "https://localhost:5000"}})

###14
#Toda la informacion sensitiva sera transmitida como datos en los headers
# para los POST el envio puede ser por el body o el header y para los GET por el header
# no es necesaria una prueba porque ya esta incluida en las funciones de los endpoints, pj loginjwtrol

###15
#Todas las solicitudes responden con el status code correspondiente

###16
# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Vehiculos API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('swagger', path)






'''class Register(Resource):

class Login(Resource):

class ModificarUsuario(Resource):

class BajaUsuario(Resource):

class Roles(Resource):

class Vehiculos(Resource):

class GenerarTarjeton(Resource):

class VerificarTarjeton(Resource):'''




class ProtectedResource(Resource):
    #@cross_origin(origins='localhost:5000')
    def get(self):
        return {'message': 'Hello, SSL-protected World!'}

class ErrorCors(Resource):
    #@cross_origin(origins='localhost:5000')
    def get(self):
        return {'message': 'Si accediste desde la ip localhost:5000 OK!'}
        
#paginas devueltas SOLO a modo de prueba de la API
@app.route('/index.html')
def extended_page():
    return render_template('vehiculos.html'),200,{'Content-Typefix': 'text/html'}
@app.route('/')
def extended_page0():
    return render_template('vehiculos.html'),200,{'Content-Typefix': 'text/html'}
@app.route('/vehiculos.css')
def extended_page2():
    return render_template('vehiculos.css')
@app.route('/API.js')
def extended_page3():
    return render_template('API.js')
@app.route('/General.js')
def extended_page4():
    return render_template('General.js')
@app.route('/jquery-3.7.1.min.js')
def extended_page5():
    return render_template('jquery-3.7.1.min.js')
@app.route('/nav.js')
def extended_page6():
    return render_template('nav.js')

api.add_resource(ProtectedResource, '/v1/protected')
api.add_resource(ProtectedResourceAPIKEY, '/v1/usuarios/protectedapikey')
api.add_resource(Login, '/v1/usuarios/login')
api.add_resource(Register, '/v1/usuarios/registrar')
api.add_resource(GetApiKey, '/v1/usuarios/getApiKey')
api.add_resource(LoginJWT, '/v1/usuarios/loginJWT')
api.add_resource(ProtectedResourceJWT, '/v1/usuarios/protectedjwt')
api.add_resource(LoginJWTROL, '/v1/usuarios/loginJWTROL')
api.add_resource(ProtectedResourceJWTAdmin, '/v1/usuarios/protectedjwtroladmin')
api.add_resource(ProtectedResourceJWTGestor, '/v1/usuarios/protectedjwtrolgestor')
api.add_resource(ProtectedResourceJWTAgente, '/v1/usuarios/protectedjwtrolagente')
api.add_resource(ErrorEmitido, '/v1/errorEmitido')
api.add_resource(ErrorCors, '/v1/cors')



'''api.add_resource(Register, '/v1/usuarios/registrar')

api.add_resource(ModificarUsuario, '/v1/usuarios/<int:idUsuario>')
api.add_resource(BajaUsuario, '/v1/usuarios/<int:idUsuario>')
api.add_resource(Roles, '/v1/roles')
api.add_resource(Vehiculos, '/v1/vehiculos/vehículos')
api.add_resource(GenerarTarjeton, '/v1/vehiculos/<int:idVehiculo>/generarTarjeton')
api.add_resource(VerificarTarjeton, '/v1/tarjetones/<int:idTarjeton>')'''

if __name__ == '__main__':
    ssl_context = create_ssl_context()
    with app.app_context():
        db.create_all()
    app.run(ssl_context=ssl_context, host='localhost',port=5000, debug=True)
    
    
    
    
    




	
	
	
	











