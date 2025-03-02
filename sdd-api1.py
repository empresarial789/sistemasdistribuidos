import json
from urllib import response
#aca esta la configuracion de la bd y claves
from config import db, app
from modelo.Usuario import Usuario
from modelo.Vehiculo import Vehiculo
from modelo.Rol import Rol
from modelo.Tarjeton import Tarjeton

from sqlalchemy import text
from flask_httpauth import HTTPBasicAuth
import os
import ssl
from flask import request, jsonify, render_template
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
import uuid

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

#ubico los certificados para HTTPS
base_dir = os.path.abspath(os.path.dirname(__file__))
cert_path = os.path.join(base_dir, 'server.crt')
key_path = os.path.join(base_dir, 'server.key')	
assert os.path.exists(cert_path), f"server.crt no encontrado en {cert_path}"
assert os.path.exists(key_path), f"server.key no encontrado en {key_path}"

def create_ssl_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path, password='password1')
    return context

#web services endpoints

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

#funcion llamada en caso de error de autenticacion
@auth.error_handler
def auth_error(status):
    
    return {'message': 'Usuario invalido'}, status, {'Content-Type': 'text/plain'}

@app.after_request
def remove_header(response):
    #para que en las solicitudes de autentication basic no lance el browser el cartel de credenciales
    del response.headers['Www-authenticate']
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
        #rol = request.headers.get('rol')
        rol = 2

        if not username or not password:
            return {'message': 'Username y password son requeridos'}, 400
        
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
        username = request.headers.get('usuario')
        password = request.headers.get('password')
        
        if not username or not password:
            return {'message': 'Usuario y password son requeridos'}, 400

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
        
        access_token = create_access_token(identity=username)
        return {'message': 'Usuario logeado','access_token': access_token}, 200

class ProtectedResourceJWT(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hello, {current_user}'}, 200

'''class Register(Resource):

class Login(Resource):

class ModificarUsuario(Resource):

class BajaUsuario(Resource):

class Roles(Resource):

class Vehiculos(Resource):

class GenerarTarjeton(Resource):

class VerificarTarjeton(Resource):'''

class ProtectedResource(Resource):
    def get(self):
        return {'message': 'Hello, SSL-protected World!'}
        
#paginas devueltas SOLO a modo de prueba de la API
@app.route('/index.html')
def extended_page():
    return render_template('vehiculos.html')
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
    
    
    
    
    




	
	
	
	











