import serial
from os import system
from time import sleep
import re
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as fan
from itertools import count 
import csv



arduinoPoit = serial.Serial('COM7',115200)
x_vals = list(range(1000))
BigBuffer = [0]*1000
fig,ax1 = plt.subplots()
plt.style.use("fivethirtyeight")
counter = count()

fileName = open("./tstData.csv",'w')
fileName.close()

def StackBuffer(data,BigBuffer):
    data = data.split(",")
    data  = data[1:-1]
    numData = []
    for string in data:
        try:
            numData.append(int(string))
        except:
            pass

    print (BigBuffer[:10])
    BigBuffer = list(map(str,numData))+BigBuffer
    BigBuffer = BigBuffer[len(numData):]
    print (BigBuffer[:10])
    return BigBuffer,data

while True:

    with open("./tstData.csv",'a') as fileName:
        sleep(0.5)
        msg = arduinoPoit.read_until('t',16)
        data = str(msg).split("'")[1]
        BigBuffer,data = StackBuffer(data,BigBuffer)
        print (data)
        for num in data:
            fileName.write(str(num)+'||')
        fileName.write('\n')
        sleep(0.1)
        #BigBuffer,x_vals = StackBuffer(data,BigBuffer,x_vals) 
           
