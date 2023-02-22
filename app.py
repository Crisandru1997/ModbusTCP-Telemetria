from flask import Flask, render_template, jsonify
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
#from models.db_model import Temperature, db
import struct
import datetime
#import socket
#import flask


app = Flask(__name__)
# Configuración de la base de datos de NAS MySQL para Flask SQLAlchemy.
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://crisandru:12345@localhost/modbustcp'

#db.init_app(app)

# Configuración de la conexión Modbus TCP/IP.
IP_ADDRESS = "10.10.100.254" # Nueva dirección IP, esta viene por defecto.
#IP_ADDRESS = "192.168.0.101"
PORT = 502
ADDRESS = 3131


client = ModbusTcpClient(IP_ADDRESS, PORT)
#client.socket.settimeout(10.0)  # Configurar tiempo de espera de 10 segundos
client.connect()

#if client.is_socket_connected():
#    client.socket.settimeout(10.0)  # Configurar tiempo de espera de 10 segundos
#else:
#    print("No se ha podido establecer la conexión con el dispositivo Modbus")
    
# Ruta de la página principal.
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/temperature")
def temperature():
    try:
        if client.connect():
            result = client.read_holding_registers(ADDRESS, 2, slave=2)
            raw_data = struct.pack("!2H", *result.registers)
            temp = struct.unpack('!f', raw_data)[0]
            temperature_formatted = "{:.2f} °C".format(temp)
        else:
            temperature_formatted = "Error de conexión con el dispositivo Modbus"
    except ModbusIOException as e:
        print("Error de comunicación con el dispositivo Modbus:", e)
        temperature_formatted = "Error de comunicación con el dispositivo Modbus"

    # Guardar la temperatura en la base de datos
    #temperature_record = Temperature(temperature=temperature, timestamp=datetime.datetime.now())
    #db.session.add(temperature_record)
    #db.session.commit()

    return jsonify(temperature=temperature_formatted)

@app.route("/temperature_average")
def temperature_average():
    # Obtener la temperatura media de los últimos 5 minutos
    five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5) # 5 minutos atrás
    #temperatures = Temperature.query.filter(Temperature.timestamp >= five_minutes_ago).all() # Temperaturas de los últimos 5 minutos
    #average_temperature = sum(t.temperature for t in temperatures) / len(temperatures) # Temperatura media de los últimos 5 minutos
    #average_temperature_formatted = "{:.2f} °C".format(average_temperature) # Temperatura media de los últimos 5 minutos formateada
    #return jsonify(average_temperature=average_temperature_formatted) # Devolver la temperatura media de los últimos 5 minutos formateada
    return jsonify(average_temperature="0.00 °C")
    
if __name__ == "__main__":
    app.run(debug=True)
