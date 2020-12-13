import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import RPi.GPIO as GPIO
import time
import datetime
import mysql.connector
import serial

GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT)

mydb = mysql.connector.connect(
#podaci su uklonjeni 13.12.2020.
)

ser = serial.Serial('/dev/ttyACM0',9600)

temp = "" #pyzbar ume da za 1 sekundu očita isti qr kod 10tak puta, da se kapija ne bi otvarala 10 buta postoji temp koji uzima vrednost očitanog koda

################################################################################################

snimak = cv2.VideoCapture(0)

while True:
    _, frame = snimak.read()
    dekodirano = pyzbar.decode(frame)
    for x in dekodirano:
        
        print("Data: ", x.data)
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Rezervacije")
        rezervacije = mycursor.fetchall()
        
        for y in rezervacije:
            print(temp)
            if(str(x.data) == "b'" + str(y[2]) + "'" and temp != str(x.data)): 
                print('Otvaranje kapije!')
                GPIO.output(13,GPIO.HIGH)
                ser.flushInput()
                ser.write("2".encode('utf-8'))
                time.sleep(1)
                mycursor = mydb.cursor()
                mycursor.execute("DELETE FROM Rezervacije WHERE id = " + str(y[0]) + "")
                mydb.commit()
                time.sleep(2)
                GPIO.output(13,GPIO.LOW)
                temp = str(x.data)

                
    #cv2.imshow("Frame: ", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break    
