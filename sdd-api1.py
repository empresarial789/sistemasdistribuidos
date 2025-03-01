import json
#from ..back import config  #aca esta la configuracion de la bd y claves
from config import db, app
from modelo.Usuario import Usuario
from modelo.Vehiculo import Vehiculo
from modelo.Rol import Rol
from modelo.Tarjeton import Tarjeton

from sqlalchemy import text

from flask import request, jsonify
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash

api = Api(app)

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
for i in range(0, 2):
    hashed_password = generate_password_hash('password'.join(str(i)))
    new_user = Usuario(username='user'.join(str(i)), password=hashed_password,idRol = 1)
    db.session.add(new_user)


new_vehiculo = Vehiculo(dominio = 'AG071MT',segmento = 'SEDAN',marca ='TOYOTA',modelo ='Corolla 1.8 XEI L/20 CVT HYBRID',motor ='2ZR2T66831',chasis = '9BRBZ3BE1P4046263',año = '2023')
db.session.add(new_vehiculo)
new_vehiculo = Vehiculo(dominio = 'AG071MW',segmento = 'SEDAN',marca ='TOYOTA',modelo ='Corolla 1.8 XEI L/20 CVT HYBRID',motor ='2ZR2T63812',chasis = '9BRBZ3BE7P4046185',año = '2023')
db.session.add(new_vehiculo)
new_vehiculo = Vehiculo(dominio = 'AG071NF',segmento = 'UTILITARIO',marca ='RENAULT',modelo ='Kangoo II Express Confort 5A 1.6 SCE',motor ='H4MJ759Q238991',chasis = '8A18SRYD4RL703220',año = '2023')
db.session.add(new_vehiculo)
new_vehiculo = Vehiculo(dominio = 'AG071NI',segmento = 'UTILITARIO',marca ='RENAULT',modelo ='Kangoo II Express Confort 5A 1.6 SCE',motor = 'H4MJ759Q231805',chasis = '8A18SRYD4RL680781',año = '2023')
db.session.add(new_vehiculo)

new_Rol = Rol(nombreRol = 'Admin')
db.session.add(new_Rol)
new_Rol = Rol(nombreRol = 'Gestor')
db.session.add(new_Rol)
new_Rol = Rol(nombreRol = 'Agente')
db.session.add(new_Rol)

db.session.commit()
	
#web services endpoints

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
        
api.add_resource(ProtectedResource, '/protected')
        
'''api.add_resource(Register, '/v1/usuarios/registrar')
api.add_resource(Login, '/v1/usuarios/login')
api.add_resource(ModificarUsuario, '/v1/usuarios/<int:idUsuario>')
api.add_resource(BajaUsuario, '/v1/usuarios/<int:idUsuario>')
api.add_resource(Roles, '/v1/roles')
api.add_resource(Vehiculos, '/v1/vehiculos/vehículos')
api.add_resource(GenerarTarjeton, '/v1/vehiculos/<int:idVehiculo>/generarTarjeton')
api.add_resource(VerificarTarjeton, '/v1/tarjetones/<int:idTarjeton>')'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost',port=5000, debug=True)
    
    
    
    
    




	
	
	
	











