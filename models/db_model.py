from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Corriente(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary_key=True es para que el id sea autoincrementable.
    corriente = db.Column(db.Float) # db.Float es para que la temperatura sea un número decimal.
    timestamp = db.Column(db.DateTime) # db.DateTime es para que la fecha sea un formato de fecha y hora.

    def __init__(self, corriente, timestamp=None):
        self.corriente = corriente
        # Si no se especifica la fecha y hora, se toma la fecha y hora actual.
        if timestamp is None:
            timestamp = datetime.utcnow()
        # Se guarda la fecha y hora en el atributo timestamp.
        self.timestamp = timestamp
