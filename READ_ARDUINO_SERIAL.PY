import serial
from os import system
from time import sleep
import re
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as fan
from itertools import count 


nums = 500*[0]
x = list(range(500))
plt.style.use("fivethirtyeight")
counter = count()
fig, ax = plt.subplots()
ln1 = ax.plot([],[],'ro')[0]
print (ln1)
def animate(i):
    text = fileName.readline()
    text = text.split('||')

    for num in text:
        try:
            nums.append(int(num))
            x.append(next(counter))
            if len(nums)>500:
                nums.pop(0)
                x.pop(0)
        except:
            pass

    ax.cla()
    ax.plot(x,nums)
    
      

    
with open("C:/Users/shabe/OneDrive/Documents/iaac/sem12/hardware/PYSCRIPTS/tstData.csv",'r') as fileName:   
    
    ani = fan(fig,animate,interval = 25)
    plt.show()
    fileName.truncate()
