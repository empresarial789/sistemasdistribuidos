#modulo del modelo de datos
#modelo.py
from config import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    idUsuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    idRol = db.Column(db.Integer, nullable=False) #quitar nullable si uso relaciones automaticas
    def __repr__(self):
        return f'<Usuario {self.username}>'
