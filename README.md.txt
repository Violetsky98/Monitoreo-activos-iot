# Sistema IoT de Monitoreo de Activos de una Consultora Tecnológica

Este proyecto implementa una solución de **Internet de las Cosas (IoT)** y **Edge Computing** diseñada para una empresa consultora. El sistema automatiza el registro, control e inventario de activos tecnológicos (laptops, proyectores, impresoras y routers) mediante tecnología RFID, mensajería MQTT, almacenamiento relacional en SQLite y visualización en tiempo real a través de Node-RED.

---

## 🔗 Simulación Interactiva en Wokwi
Puedes probar el funcionamiento del hardware y la transmisión MQTT en tiempo real directamente en tu navegador:
 **[Abrir Simulación del Proyecto en Wokwi](https://wokwi.com/projects/477513388104728577)**

---

##  Arquitectura del Sistema

El sistema sigue un flujo desacoplado de **5 capas**:

`[Etiqueta RFID del Activo]` ➔ `[Lector RC522 + ESP32]` *(Edge Computing)* ➔ `[Broker MQTT HiveMQ Public]` *(Transporte)* ➔ `[Servidor Python]` *(Procesamiento y Persistencia)* ➔ `[SQLite - activos.db]` *(Base de Datos)* ➔ `[Node-RED Dashboard]` *(Interfaz HMI)*

---

## Lista de Materiales y Componentes (BOM)

| Componente | Tipo | Especificación Técnica | Función | Cant. |
| :--- | :--- | :--- | :--- | :---: |
| **ESP32 DevKit v1** | Hardware | 38 Pines, Wi-Fi 2.4 GHz, Dual Core 240 MHz | Procesamiento Edge, lectura SPI de RFID y cliente MQTT | 1 |
| **Lector MFRC522** | Hardware | Frecuencia 13.56 MHz, Interfaz SPI, Voltaje 3.3V | Adquisición del identificador único (UID) de tarjetas RFID | 1 |
| **Tarjetas / Tags RFID** | Hardware | Protocolo ISO/IEC 14443A, 13.56 MHz, Memoria 1 KB | Identificador físico instalado en los activos tecnológicos | 4 |
| **Broker MQTT HiveMQ** | Software / Nube | Host: `broker.hivemq.com`, Puerto 1883 | Capa de transporte y mensajería desacoplada | 1 |
| **Python 3.x + SQLite3** | Software / Backend | Módulos: `paho-mqtt`, `sqlite3`, `json`, `datetime` | Backend de procesamiento, lógica de negocio y persistencia | 1 |
| **Node-RED + Dashboard** | Software / HMI | Node.js Runtime, Nodos: `mqtt-in`, `ui_template` | Interfaz gráfica HMI en tiempo real para el usuario final | 1 |

---

## Estructura del Repositorio

```text
consultora/
├── README.md                           # Documentación principal del proyecto
├── requirements.txt                    # Dependencias de Python (paho-mqtt)
├── .gitignore                          # Archivos excluidos del control de versiones
├── wokwi/
│   ├── sketch.ino                      # Código C++ del ESP32 (Lectura RFID y MQTT)
│   └── diagram.json                    # Diagrama de conexiones en Wokwi
├── backend/
│   ├── app_procesamiento.py            # Script Python (Suscriptor MQTT y SQLite)
│   └── schema.sql                      # Estructura e inserciones iniciales de la BD
└── nodered/
    └── flows.json                      # Flujo completo exportado de Node-RED