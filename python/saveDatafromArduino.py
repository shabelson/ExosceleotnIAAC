import serial
import time
import csv

ser = serial.Serial("COM5",9600)
ser.flushInput()
startTime = time.time()
`with open("test_data.csv","w") as f:
    while True:
        
        try:
            ser_bytes = ser.readline()
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            print(decoded_bytes)
            currentTime = time.time() - startTime
            roundTime = round(currentTime,2)
            writer = csv.writer(f,delimiter=",")
            writer.writerow([decoded_bytes,roundTime])
        except Exception as e: 
            print (e)
            print("keyboard interrupt")
            break