#modulo del modelo de datos
#modelo.py
from config import db

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    idVehiculo = db.Column(db.Integer, primary_key=True)
    dominio = db.Column(db.String(25), unique=True, nullable=False)
    segmento = db.Column(db.String(25), nullable=False)
    marca = db.Column(db.String(25), nullable=False)
    modelo = db.Column(db.String(60), nullable=False)
    motor = db.Column(db.String(25), nullable=False)
    chasis = db.Column(db.String(25), nullable=False)
    año = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f'<Vehiculo {self.dominio}>'
