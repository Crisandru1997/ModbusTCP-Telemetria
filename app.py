from flask import Flask, render_template, jsonify
from pymodbus.client import ModbusTcpClient
from models.db_model import Temperature, db
import struct
import datetime

app = Flask(__name__)
# Configuración de la base de datos de NAS MySQL para Flask SQLAlchemy.
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cris:12345@192.168.0.105/cris_temperatura'

#db.init_app(app)

# Configuración de la conexión Modbus TCP/IP.
IP_ADDRESS = "10.10.100.254"
PORT = 502
ADDRESS = 3131

client = ModbusTcpClient(IP_ADDRESS, PORT)
client.connect()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/temperature")
def temperature():
    result = client.read_holding_registers(ADDRESS, 2, slave=2)
    raw_data = struct.pack("!2H", *result.registers)
    temperature = struct.unpack("!f", raw_data)[0]
    temperature_formatted = "{:.2f} °C".format(temperature)
    
    #temperature_record = Temperature(temperature=temperature, timestamp=datetime.datetime.now())
    #db.session.add(temperature_record)
    #db.session.commit()
    return jsonify(temperature=temperature_formatted)

if __name__ == "__main__":
    app.run(debug=True)
