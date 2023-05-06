import struct
import paho.mqtt.client as paho
from paho import mqtt

# Calbacks -------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s.\nThe response flag is: %s" % (rc, flags))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid))
    print( granted_qos[0] )

def on_message(client, userdata, msg):
    data = msg.payload.decode
    print(msg.topic + " " + str(msg.qos) + ": " + msg.payload)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))
# end of callbacks ----------------------------------------------------------------



def main() -> None:
    device_id = 1
    temperature = 7
    turbidite = 3
    latitude = 3.7749
    longitude = -18.7117
    altitude = 0.5
    rssi = -102
    snr = 999

    #b'\x07\x03\x00\x00\xf6\x97q@\x90\xb1\x95\xc1\x00\x00\x00?\x00\x00\xcc\xc2\t'
    packed_data = struct.pack('b2f2d2fd',device_id, temperature, turbidite, latitude, longitude, altitude, rssi, snr)
    client = paho.Client(client_id="", userdata=None)
    client.on_connect = on_connect
    
    # connect to HiveMQ Cloud on port 8883 
    # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("aquarob", "aquarob")
    # client.connect("948d5240da044a759077ffa5e4b8d98a.s2.eu.hivemq.cloud", 8883)

    client.connect("172.17.0.2", 9000)
    
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    client.publish("/testpython", payload=packed_data, qos=1)
    client.loop_forever()
    


if __name__  == "__main__":
    main()


