import paho.mqtt as mqtt
from paho.mqtt import client 
import time

import serial
import atexit




def LoadJson():
    path = "//"

    name = "Mqtt_dets.json"

    fileName = os.path.join(path,name)

    with open(fileName) as json_file: 

        data = json.load(json_file) 

    return data


def GetAllTopics(data,pubsub = "sub"):
    topDict = {}
    
    topTup =[]
    
    if pubsub =="pub" :  topFilter = "sense"
    
    else: topFilter = "robo"
    
    for subTop in  data["Topics"]:
    
        key = subTop["name"]
    
        try:
    
            if not key.split("_") == topFilter:continue
    
        except: 
    
            continue 
    
        del subTop["name"]
    
        for tp in subTop.keys():
    
            subTop[tp] = key +"/"+ subTop[tp]

            topTup.append((subTop[tp],1))

        topDict.update({key:subTop})

    return topDict,topTup


def doAtExit():
    serialArduino.close()
    print("Close serial")
    print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))


def ReadFromArduino(serialArduino):
    packet = serialArduino.readline(500)[1:-1]
    








serverDict = LoadJson()

topDict,topList = GetAllTopics(serverDict)

client = client.Client("raspy_sense")

client.connect(serverDict["BrokerIP"])







values = []

cnt=0

serialArduino = serial.Serial("", 9600)


atexit.register(doAtExit)
    
while True:
    while (serialArduino.inWaiting()==0):
        pass
    #print("readline()")
    valueRead = ReadFromArduino(serialArduino)

    #check if valid value can be casted
    try:
        valueInInt = int(valueRead)
        print(valueInInt)
        if valueInInt <= 1000:
            if valueInInt >= 0:
                values.append(valueInInt)
                values.pop(0)
                drawnow(plotValues)
            else:
                print("Invalid! negative number")
        else:
            print("Invalid! too large")
    except ValueError:
        print("Invalid! cannot cast")




try:
    while True:
        client.loop_start()
        client.publish("sha","yo yo yo wii")
        client.loop_stop()
except:
        client.loop_stop()
