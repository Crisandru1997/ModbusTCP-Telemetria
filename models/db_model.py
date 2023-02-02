from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

app = Flask(__name__)
# Configuración de la base de datos MySQL para Flask SQLAlchemy.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cris:12345@192.168.0.105/cris_temperatura'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary_key=True es para que el id sea autoincrementable.
    temperature = db.Column(db.Float) # db.Float es para que la temperatura sea un número decimal.
    timestamp = db.Column(db.DateTime) # db.DateTime es para que la fecha sea un formato de fecha y hora.

    def __init__(self, temperature, timestamp=None):
        self.temperature = temperature
        # Si no se especifica la fecha y hora, se toma la fecha y hora actual.
        if timestamp is None:
            timestamp = datetime.utcnow()
        # Se guarda la fecha y hora en el atributo timestamp.
        self.timestamp = timestamp

if __name__ == '__main__':
    from models.db_model import db
    db.create_all()
    app.run(debug=True)
