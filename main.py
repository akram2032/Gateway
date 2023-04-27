# TODO(akram): error handling ei. temp = -1 ==> an error has occured
import mysql.connector
import struct
import paho.mqtt.client as paho
import sys
from paho import mqtt

# Mqtt connection

# Calbacks -------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("CONNACK received with code %s.\nThe response flag is: %s" % (rc, flags))
    else: 
        print("Bad Connection")
    
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

    device_id,temp, turbidite, latitude, longitude, altitude, rssi, snr = struct.unpack('b2f2d2fd', msg.payload)
    data = f"""Recived Data:\nTemperature: {temp}.\n turbidite:{turbidite}\n.
    latitude:{latitude}.\nlongitude: {longitude}.\nAltitude: {altitude}.\n
    Rssi/Snr: {rssi}, {snr}.\n"""
    
    sql = f"""INSERT INTO aquaRob2(device_id, temperature, longetude, latitude,
                                     altitude, rssi,  snr, turbidite) Values(
                {device_id},{temp}, {longitude}, {latitude}, {altitude}, {rssi}, {snr}, {turbidite}
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
    topic,username,password = sys.argv[1:4]    
    # connect to HiveMQ Cloud on port 8883 
    #client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    #client.username_pw_set("aquarob", "aquarob203")
    #client.connect("948d5240da044a759077ffa5e4b8d98a.s2.eu.hivemq.cloud", 8883)

    # connect the a local broker
    try:
        client.username_pw_set(username,password)
        client.connect("0.0.0.0",port=9000)
    except:
        print("An error has occured check your credentials an retry\n")
        exit()
    print(f"Subscribed to /{topic}")
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.subscribe(f"/{topic}", qos=1)
    client.loop_forever()
    return 0 

if __name__ == "__main__":
    help_ = """Software usage: 
python main.py |sub_Topic| |username| |password|
        """
    if len(sys.argv) == 4: 
        print(f"topic {sys.argv[1]}.\nusername {sys.argv[2]}.\npassword {sys.argv[3]}")
        main()
    print (help_)
    exit()

