
import paho.mqtt as mqtt
from paho.mqtt import client 
from time import sleep
import os
import json 
import time
import csv
import EMGfunctions as emgf
import traceback as tb


global emgBuff
global timeBuff
emgBuff = []
timeBuff = []
startTime = time.time()
def EMG_SUB(decoded_bytes):
    
    emgBuff.append(decoded_bytes)
    currentTime = time.time() - startTime
    roundTime = round(currentTime,2)
    timeBuff.append(currentTime)
    if len(emgBuff) >20:
        emgBuff.pop(0)
        timeBuff.pop(0)
        emgcorrectmean = emgf.remove_mean(emgBuff,timeBuff)
        emg_filtered = emgf.emg_filter(emgcorrectmean, timeBuff)
        emg_rectified = emgf.emg_rectify(emg_filtered, timeBuff)
        emg_filtered, emg_envelope = emgf.alltogether(timeBuff,emgBuff, low_pass=2, sfreq=1000, high_band=20, low_band=450)
    
    
        finValue = sum(emg_rectified)/len(emg_rectified)
    else:
        finValue = decoded_bytes
    try:
        f = open("test_data.csv","a")    
    except:
        f = open("test_data.csv","w")
    try:
        print ("START RECORD")

        writer = csv.writer(f,delimiter=",")
        writer.writerow([finValue,roundTime])
        print ("recorded")
    except Exception as e: 
        print (e)
    finally:
        f.close()

    #avg = sum([int(t) for t in emgBuff])/len(emgBuff)
    

    return finValue



def IMU_SUB(payload):
    pass
def Finger_SUB(payload):
    pass
def Pneumatic_SUB(payload):
    pass



def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    
    if message.topic =="emg_sense/emg":
        EMG_SUB(message.payload.decode("utf-8"))
def on_log(client, userdata, level, buf):
    #print("log: ",buf)
    pass



def LoadJson():
    path = "G:\\My Drive\\team2_software_sysData\\"

    name = "Mqtt_dets.json"

    fileName = os.path.join(path,name)

    with open(fileName) as json_file: 

        data = json.load(json_file) 

    return data


def GetAllTopics(data,pubsub = "sub"):
    topDict = {}
    
    topTup =[]
    
    emg_filter = "emg"
    if pubsub =="pub" :  topFilter = "sense"
    
    else: topFilter = "robo"
    
    for subTop in  data["Topics"]:
    
        
        key = subTop["name"]
        
        try:
            
            if not key =="emg_sense":continue
            #if not key == "emg_sense":continue ### TODO - ONLY FOR 2nd iteration
            #if not key.split("_")[1] == topFilter: continue
            
        except: 
            continue 
    
        del subTop["name"]
    
        for tp in subTop.keys():
            
            subTop[tp] = key +"/"+ subTop[tp]

            topTup.append((subTop[tp],1))

        topDict.update({key:subTop})

    return topDict,topTup






serverDict = LoadJson()

topDict,topList = GetAllTopics(serverDict)

client = client.Client("PC_1")

client.connect(serverDict["BrokerIP"])

client.on_log=on_log

client.on_message = on_message



while True: 
    #sleep (0.5)

    client.loop_start()
    #emgcorrectmean = emgf.remove_mean(emgBuff,timeBuff)
    #emg_filtered = emgf.emg_filter(emgcorrectmean, timeBuff)
    #emg_rectified = emgf.emg_rectify(emg_filtered, timeBuff)
    client.subscribe(topList)
    
    client.loop_stop()
