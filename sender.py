import struct
import socket

temperature = 7
turbidite = 3
latitude = 3.7749
longitude = -18.7117
altitude = 0.5
rssi = -102
snr = 9

host = socket.gethostbyname(socket.gethostname())
port = 12345
# b4e b'%\x00\xb9PV\xd8@I \xd8'
packed_data = struct.pack('2b4fb', temperature, turbidite, latitude, longitude, altitude, rssi, snr)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((host, port))
connection.send(packed_data)
connection.close()
