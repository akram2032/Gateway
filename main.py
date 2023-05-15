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
        print("Connected.")
    else: 
        print("Bad Connection")


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid))
    print("Granted QOS: %s"%granted_qos[0] )


def on_message(client, userdata, msg):
    # DataBase connection
    try:
        mydb = mysql.connector.connect(
            host="mysql-akram203.alwaysdata.net",
            user="akram203",
            password="akram2001",
            database="akram203_pfe"
        )
        cursor = mydb.cursor()
    except mysql.connector.errors.InterfaceError:
        print('Error while trying to connect to the dataBase')
        return

    try:
        print("message: ",msg.payload)
        device_id, temp, turbidite, latitude, longitude, altitude, rssi, snr = struct.unpack('B5fdb', msg.payload)
        # device_id,temp, turbidite, latitude, longitude, altitude, rssi, snr =  msg.payload.decode()
        data = f"""\nRecived Data:\n----------------\nTemperature: {temp}.\nTurbidity:{turbidite}\nLatitude:{latitude}.\nlongitude: {longitude}.\nAltitude: {altitude}.\nDistance  {distance}.\n"""
        print(data)

    except struct.error:
        print(f"Recived data : {msg.payload}")
        print('Error on data format')
        return

    except:
        print("errorG")


    try:
        sql = f"""INSERT INTO aquaRob2(device_id, temperature, longetude, latitude,
                                     altitude, rssi,  snr, turbidite) Values(
                {device_id},{temp}, {longitude}, {latitude}, {altitude}, {rssi}, {snr}, {turbidite}
                )"""
        cursor.execute(sql)
        mydb.commit() 
        print('data inserted')
        cursor.close()
        mydb.close()
    except mysql.connector.errors.ProgrammingError:
        print("Request error => Data not inserted.")
        return 

# end of callbacks ----------------------------------------------------------------


def main() -> int:
    client = paho.Client(client_id="", userdata=None)
    client.on_connect = on_connect
    topic, username, password, ip, port_ = sys.argv[1:6]    
    # connect to HiveMQ Cloud on port 8883 
    # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # client.username_pw_set("aquarob", "aquarob203")
    # client.connect("948d5240da044a759077ffa5e4b8d98a.s2.eu.hivemq.cloud", 8883)

    # connect the a local broker
    try:
        client.username_pw_set(username,password)
        client.connect(f"{ip}",port=int(port_))
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
python main.py |sub_Topic| |username| |password| |IP addr| |port|  
        """
    if len(sys.argv) == 6: 
        print(f"Connecting to {sys.argv[4]}:{sys.argv[5]}...")
        main()
    print (help_)
    exit()

