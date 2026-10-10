import sqlite3
import json
from datetime import datetime
import paho.mqtt.client as mqtt

# Ruta absoluta a tu base de datos SQLite
DB_NAME = r"C:\Users\xsalg\OneDrive\Documentos\9 SEMESTRE\TECNOLOGIAS EMERGENTES\consultora\activos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activos (
            rfid_uid TEXT PRIMARY KEY,
            nombre_activo TEXT,
            tipo TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_activos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rfid_uid TEXT,
            usuario TEXT,
            fecha_hora TEXT,
            estado TEXT,
            ubicacion TEXT,
            FOREIGN KEY (rfid_uid) REFERENCES activos (rfid_uid)
        )
    ''')
    
    activos_iniciales = [
        ('AABBCCDD', '💻 Laptop Dell XPS 15', 'Laptop'),
        ('1A2B3C4D', '📽️ Proyector Epson 4K', 'Proyector'),
        ('5E6F7G8H', '🖨️ Impresora HP LaserJet', 'Impresora'),
        ('9I8H7G6F', '📡 Router Cisco ISR', 'Router')
    ]
    cursor.executemany('INSERT OR IGNORE INTO activos VALUES (?,?,?)', activos_iniciales)
    conn.commit()
    conn.close()

def on_connect(client, userdata, flags, rc):
    print("Conectado exitosamente al broker HiveMQ.")
    client.subscribe("empresa/activos/rfid")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        uid = data.get("uid")
        ubicacion = data.get("ubicacion", "Desconocida")
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT nombre_activo, tipo FROM activos WHERE rfid_uid = ?", (uid,))
        activo = cursor.fetchone()
        
        if activo:
            nombre = activo[0]
            tipo = activo[1]
            estado = "En préstamo / En uso"
        else:
            nombre = "Equipo No Identificado"
            tipo = "Desconocido"
            estado = "Sin Registro"
            
        usuario = "Ing. Soporte Tech"
        
        # 1. Persistencia en SQLite
        cursor.execute('''
            INSERT INTO historial_activos (rfid_uid, usuario, fecha_hora, estado, ubicacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (uid, usuario, fecha_hora, estado, ubicacion))
        conn.commit()
        conn.close()
        
        print(f"[{fecha_hora}] 🟢 REGISTRO GUARDADO EN SQLITE -> {nombre}")
        
        # 2. Publicar paquete directo para el Dashboard de Node-RED
        payload_dashboard = {
            "activo": nombre,
            "tipo": tipo,
            "usuario": usuario,
            "fecha": fecha_hora,
            "estado": estado,
            "ubicacion": ubicacion
        }
        client.publish("empresa/activos/dashboard", json.dumps(payload_dashboard))
        print("⚡ Evento enviado a Node-RED por MQTT.")

    except Exception as e:
        print("Error en procesamiento:", e)

init_db()

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except:
    client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()