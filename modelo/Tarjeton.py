#modulo del modelo de datos
#modelo.py
from config import db
    
class Tarjeton(db.Model):
    __tablename__ = 'tarjetones'
    idTarjeton = db.Column(db.Integer, primary_key=True)
    fechaAlta = db.Column(db.String(80), nullable=False)
    idVehiculo = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f'<Tarjeton {self.idTarjeton}>'