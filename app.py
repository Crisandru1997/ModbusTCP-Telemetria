from flask import Flask, render_template, jsonify
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from models.db_model import Temperature, db
import flask
import struct
import datetime
import socket
import time

app = Flask(__name__)
# Configuración de la base de datos de NAS MySQL para Flask SQLAlchemy.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cris:12345@34.176.16.130/cris_temperatura'

db.init_app(app)

# Variables
IP_ADDRESS = "192.168.0.100"
PORT = 502
ADDRESS = 136 # Corriente (media)
listado_final = list() # Listado para invertir los datos.

# Conexión con el tablero.
client = ModbusTcpClient(IP_ADDRESS, PORT)
client.connect()
if client.connect():
    print("Conectado con éxito al dispositivo Modbus")
else:
    print("Error de conexión con el dispositivo Modbus")


@app.route("/corriente")
def corriente():
    if client.connect():
        try:
            result = client.read_holding_registers(ADDRESS, 2, slave=2)
            l1 = result.registers[0]
            l2 = result.registers[1]
            listado_final.append(l2)
            listado_final.append(l1)
            raw_data = struct.pack("!2H", *listado_final)
            temp = struct.unpack('!f', raw_data)[0]
            final = "{:.5f}".format(temp)
            corriente = Corriente(corriente=final, timestamp=datetime.datetime.now())
            db.session.add(corriente)
            db.session.commit()
            listado_final = list()
        except ModbusIOException as e:
            print("Error de comunicación con el dispositivo Modbus:", e)    
    else:
        print("Error de conexión con el dispositivo Modbus")
    return jsonify(corriente=corriente)
