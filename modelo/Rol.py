#modulo del modelo de datos
#modelo.py
from config import db

class Rol(db.Model):
    __tablename__ = 'roles'
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String(15), unique=True, nullable=False)
    # the one-to-one relation
    '''usuario = relationship("Usuario", uselist=False, backref="usuario")
    rol = obtener el rol(...)
usuario1 = nuevo usuario()
usuario1.usuario = rol '''
    def __repr__(self):
        return f'<Rol {self.nombreRol}>'
