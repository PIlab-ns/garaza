from flask import Flask, render_template, request, jsonify, url_for, redirect
from bme280 import main
import RPi.GPIO as GPIO
import time
import datetime
import serial
import qrcode
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import mysql.connector
import re

#Global
mesta = ["0","0","0","0"]
mydb = mysql.connector.connect(
#obrisani podaci 13.12.2020.
)
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'#za validaciju maila

ser = serial.Serial('/dev/ttyUSB0',9600)

#Pin setup
GPIO.setmode(GPIO.BCM)
pmesto = 18 #zelena
pmesto2 = 21 #narandzasta
pmesto3 = 20 #plavo
pmesto4 = 25 #braon                                                                                                                                                                                                                                                                                                                                                                                                                                                         bg
GPIO.setup(pmesto,GPIO.IN)
GPIO.setup(pmesto2,GPIO.IN)
GPIO.setup(pmesto3,GPIO.IN)
GPIO.setup(pmesto4,GPIO.IN)
        
def Mesta():
    if (GPIO.input(pmesto) == 1):
        mesta[0] = "1"
    else:
        mesta[0] = "0"  
    if (GPIO.input(pmesto2) == 1):
        mesta[1] = "1"
    else:
        mesta[1] = "0"
    if (GPIO.input(pmesto3) == 1):
        mesta[2] = "1"
    else:
        mesta[2] = "0"
    if (GPIO.input(pmesto4) == 1):
        mesta[3] = "1"
    else:
        mesta[3] = "0"

    mycursor = mydb.cursor()
    mycursor.execute("SELECT Slobmesta FROM Rezervacije")
    rezervisana_mesta = mycursor.fetchall()
    
    for rm in rezervisana_mesta:
        red = str(rm[0])
        redd = red.zfill(4)
        for x in range(len(redd)):
            if(redd[x] == "1"):
                mesta[x] = "1"
            
def Gasovi(): 
    ser.flushInput()
    ser.write("1")
    time.sleep(1)
    x = ser.readline()

    return x

def BME():
    bme = ["","",""]
    bme = main()

    return bme

#Proverava da li su sva mesta zauzeta
def KeyCheck():
    if(mesta[0] == "1" and mesta[1] == "1" and mesta[2] == "1" and mesta[3] == "1"):
        key = 0
    else:
        key = 1

    return key

#Kreira QRkod za rezervaciju i odmah poziva funkciju za slanje e-maila
def MakeQrCode(mail_adress):
    code = qrcode.make(str(mail_adress))
    ind = random.randint(0,10000)
    code_name = 'qrcode/kod-' + str(mail_adress) + '' + str(ind) + ''
    code.save(code_name)
    SendMail(mail_adress, code_name)

    #pisanje rezervacije u bazu
    time = datetime.datetime.now()
    cur_time = time.hour * 3600 + time.minute * 60 
    rezmesto=""
    index = 0  
    for x in range(len(mesta)):
        if(index == 0):
            if(mesta[x] == "0"):
                rezmesto += "1"
                index = 1
            else:
                rezmesto += "0"
        else:
            rezmesto += "0"
            
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO Rezervacije VALUES('0',0,'" + str(code_name[11:]) + "','" + str(rezmesto) + "'," + str(cur_time) + ");")
    mydb.commit()

    os.remove(code_name)

def SendMail(mail_adress, code_file):
    SenderAdr = 'pilab.ets.gsistem@gmail.com'
    SenderPass = 'gsistem.pilab0103'
    ReceiverAdr = mail_adress

    #MIME setup
    message = MIMEMultipart()
    message['From'] = SenderAdr
    message['To'] = ReceiverAdr
    message['Subject'] = 'Rezervacija parking mesta'

    key = KeyCheck()

    if(key == 1):
        poruka = 'Vas QR-Code za pristup garazi! \nHvala sto koristite nase usluge!'

        message.attach(MIMEText(poruka,'plain'))
        file_name = code_file
        attach_file = open(file_name, 'rb').read()
        image = MIMEImage(attach_file, name='QR-Code')
        message.attach(image)

    elif(key == 0):
        poruka = 'Nije moguce izvrsiti rezervaciju, sva parking mesta su zauzeta! \nHvala sto koristite nase usluge!'
        message.attach(MIMEText(poruka,'plain'))

    #Sending email
    mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
    mailServer.starttls()
    mailServer.login(SenderAdr, SenderPass)
    text = message.as_string()
    mailServer.sendmail(SenderAdr, ReceiverAdr , text)
    mailServer.quit()

#Proverava da li je istekla rezervacija i briše je ako jeste    
def Rcheck():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Rezervacije")
    rezervacije = mycursor.fetchall()
    
    time = datetime.datetime.now()
    cur_time = time.hour * 3600 + time.minute * 60
    
    for y in rezervacije:
        if(cur_time > int(y[4]) + 60):
            mycursor = mydb.cursor()
            mycursor.execute("DELETE FROM Rezervacije WHERE id = " + str(y[0]) + "")
            mydb.commit()    
            #print("Sta sam jeo")

#Nije realizovano zbog komplikacije sa USB vezom 
'''def OtvoriKapiju():
    ser.flushInput()
    ser.write("2") #.encode('utf-8')'''

app = Flask(__name__)

@app.route('/ajax/',methods = ['GET'])
def data():
    Rcheck()
    Mesta()

    lista_bme = BME()
    temp_py = round(lista_bme[0], 2)
    pressure_py = round(lista_bme[1], 2)
    hum_py = round(lista_bme[2], 2)
    
    gas_index = Gasovi()
    
    #if(gas_index == 2):
        #OtvoriKapiju() Kapija se otvora ako je koncentracija stetnih gasova prevelika / nije realizovano zbog komplikacije sa USB vezom 

    #update tabele garaze
    mestavalue = mesta[0] + mesta[1] + mesta[2] + mesta[3]
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE Garaze SET Slobmesta = '" + mestavalue + "', Temperatura= " + str(temp_py) + ", VlVazduha = " + str(hum_py) + ", Vpritisak = " + str(pressure_py) + ", StanjeGasova = " + str(gas_index) + ";")
    mydb.commit()

    return jsonify(m1 = mesta[0], m2 = mesta[1], m3 = mesta[2], m4 = mesta[3], temp_js = temp_py, pressure_js = pressure_py , hum_js = hum_py, gas_js = gas_index)

@app.route('/')
def home():
	return render_template("login.html")    

@app.route('/login', methods=['GET', 'POST'])
def login():
    index = request.form
    if(index["username"]=="Admin" and index["password"]=="pilab01"):	
        return render_template("index.html")
    else:
	    return render_template("login.html", txt="Pogresan username ili password")

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    form_data = request.form
    email = form_data["email"]
    key2 = KeyCheck()
    if(re.search(regex,email) and key2 == 1):
        MakeQrCode(str(email))
    
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
