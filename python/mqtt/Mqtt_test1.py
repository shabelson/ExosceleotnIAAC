import paho.mqtt as mqtt
from paho.mqtt import client 
import time


client = client.Client("test1")
client.connect("172.16.22.145",1883)
try:
    while True:
        client.loop_start()
        client.publish("sha","yo yo yo wii")
        client.loop_stop()
except:
        client.loop_stop()
