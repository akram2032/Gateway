import mysql.connector
import socket
import struct
# import logging
# import io

# Base de donnee
mydb = mysql.connector.connect(
    host="mysql-akram203.alwaysdata.net",
    user="akram203",
    password="akram2001",
    database="akram203_pfe"
)
cursor = mydb.cursor()

# connection socket
host = socket.gethostbyname(socket.gethostname())
port = 12345
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((host, port))
soc.listen(1)
print(f'Listening on {host}:{port}')
while True:
    connection, address = soc.accept()
    print(f'Connected by {address[0]}')
    while True:
        data = connection.recv(30)
        if not data:
            break
        temp, turbidite, latitude, longitude, altitude, rssi, snr = struct.unpack('2b4fb', data)
        sql = f"""INSERT INTO aquaRob2(temperature, longitude, latitude,
                                     altitude, rssi,  snr, turbidite) Values(
                {temp}, {longitude}, {latitude}, {altitude}, {rssi}, {snr}, {turbidite}
                )"""
        cursor.execute(sql)
        mydb.commit() 
        print('data inserted')
    cursor.close()
    mydb.close()
    connection.close()
