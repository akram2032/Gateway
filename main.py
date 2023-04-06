# TODO(akram): error handling ei. temp = -1 ==> an error has occured
import mysql.connector
import socket
import struct
import paho.mqtt.client as paho
from paho import mqtt

# Mqtt connection

# Calbacks -------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s.\nThe response flag is: %s" % (rc, flags))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid))
    print( granted_qos[0] )

def on_message(client, userdata, msg):
    #DataBase connection
    mydb = mysql.connector.connect(
        host="mysql-akram203.alwaysdata.net",
        user="akram203",
        password="akram2001",
        database="akram203_pfe"
    )
    cursor = mydb.cursor()

    temp, turbidite, latitude, longitude, altitude, rssi, snr = struct.unpack('2b4fb', msg.payload)
    data = f"""Recived Data:\nTemperature: {temp}.\n turbidite:{turbidite}\n.
    latitude:{latitude}.\nlongitude: {longitude}.\nAltitude: {altitude}.\n
    Rssi/Snr: {rssi}, {snr}.\n"""
    
    sql = f"""INSERT INTO aquaRob2(temperature, longitude, latitude,
                                     altitude, rssi,  snr, turbidite) Values(
                {temp}, {longitude}, {latitude}, {altitude}, {rssi}, {snr}, {turbidite}
                )"""
    cursor.execute(sql)
    mydb.commit() 
    print('data inserted')
    cursor.close()
    mydb.close()

# end of callbacks ----------------------------------------------------------------

def main() -> int:
    client = paho.Client(client_id="", userdata=None)
    client.on_connect = on_connect
    
    # connect to HiveMQ Cloud on port 8883 
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("aquarob", "aquarob203")
    client.connect("948d5240da044a759077ffa5e4b8d98a.s2.eu.hivemq.cloud", 8883)

    # connect the a local broker
    #client.connect("0.0.0.0", 1883)
    
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.subscribe("/aquaRob", qos=1)
    client.loop_forever()
    return 0 

if __name__ == "__main__":
    main()

