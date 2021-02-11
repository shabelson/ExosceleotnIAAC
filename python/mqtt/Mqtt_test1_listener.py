
import paho.mqtt as mqtt
from paho.mqtt import client 
from time import sleep

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
def on_log(client, userdata, level, buf):
    print("log: ",buf)
client = client.Client("test2")
client.connect("172.16.22.145")
client.on_log=on_log
msg = client.on_message = on_message
while True: 
    client.loop_start()
    client.subscribe("sha")
    sleep(0.5)
    client.loop_stop()