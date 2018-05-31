#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20180530
# Version:   1.0
# Homepage:   https://www.custom-build-robots.com
# Dieses Programm ermoeglicht es einen mobilen Roboter
# auf Basis eines Raspberry Pi Computers zu steuern.

import sys
import os
import time
import string
#import struct
#import datetime

from flask import Flask, jsonify, render_template, request

# Mit diesem Aufruf sucht Python im angegebenen Ordner nach 
# weiteren Modulen die importiert werden koennen.
sys.path.append("/home/pi/robot")

# Das Programm L298NHBridge.py wird als Modul geladen. Es stellt
# die Funktionen fuer die Steuerung der H-Bruecke zur Verfuegung.
import L298NHBridge as HBridge

app = Flask(__name__)

# Diese Funktion schaltet den Raspberry Pi ab.				
def shutdownpi():
	os.system("sudo halt &")

# Diese Funktion startet den Raspberry Pi neu.
def rebootpi():
	os.system("sudo reboot &")

# Initialisieren der Variablen und Definition dieser als global so dass
# sie allen anderen Programmteilen zur Verfuegung stehen.
def initiate():
    global speedleft
    global speedright
    global step
    global error_msg
    error_msg = ""
    # Variablen Definition der Geschwindigkeit der linken und rechten 
    # Motoren des Roboter-Autos.
    speedleft = 0
    speedright = 0
    # Die Variable "step" legt die Schrittweite der Beschleunigung 
    # fest. Mit jedem Aufruf ueber die Web-Steuerung wird die 
    # Geschwindigkeit im Wert der Variable step veraendert 
    step = 0.1

# Die Entgegennahme von Befehlen aufgerufen auf der Web-Oberflaeche
# wird ueber @app.route('<URL>') durch Flask realisiert.
# Anschließend werden die hinter jedem Aufruf hinterlegten Befehle
# abgearbeitet und ermoeglichen so eine Steuerung des Roboters

# Hier folgt der Abschnitt fuer den Flask Web-Server.

@app.route('/')
def index():
	return render_template('index.html')

# Die Funktion "halt()" legt fest, dass der Raspberry Pi
# heruntergefahren wird und ausgeschalten werden kann.
@app.route('/halt/', methods=['GET'])
def halt():
    shutdownpi()
    ret_data = {"value": "Halt button pressed."}
    return jsonify(ret_data)  

# Die Funktion "reboot()" legt fest, dass der Raspberry Pi
# neustartet.
@app.route('/reboot/', methods=['GET'])
def reboot():
    rebootpi()	
    ret_data = {"value": "Reboot button pressed."}
    return jsonify(ret_data) 
   
# Die Funktion "ButtonForward()" legt fest, dass das Roboter
# Auto vorwaerts faehrt.
@app.route('/forward/', methods=['GET'])
def ButtonForward():
    global speedleft
    global speedright

    # Das Roboter-Auto wird beschleunigt bzw. es faehrt vorwaerts.
    speedleft = speedleft + step
    speedright = speedright + step

    # Die Geschwindigkeit darf nicht groesser als +1 werden. 
    # Der Bereich der Geschwindigkeit liegt zwischen -1 und +1.
    if speedleft > 1:
        speedleft = 1
    if speedright > 1:
        speedright = 1

    # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke
    HBridge.setMotorLeft(speedleft)
    HBridge.setMotorRight(speedright)

    # Mit diesem Aufruf wird an die Web-Oberflaeche zurueck gegeben
    # welcher Button zuletzt gedrueckt wurde.
    ret_data = {"value": "Forward button pressed."}
    return jsonify(ret_data) 
      
# Die Funktion "ButtonBackward()" legt fest, dass das Roboter  
# Auto rueckwaerts faehrt.
@app.route('/backward/', methods=['GET'])
def ButtonBackward():   
    global speedleft
    global speedright

    # Das Roboter-Auto wird abgebremst bzw. es faehrt rueckwaerts.
    # Der Bereich der Geschwindigkeit liegt zwischen +1 fuer die vorwaerts
    # Fahrt und -1 fuer die rueckwaerts Fahrt des Roboter-Autos.   
    speedleft = speedleft - step
    speedright = speedright - step

    # Die Geschwindigkeit darf nicht kleiner als -1 werden.
    if speedleft < -1:
        speedleft = -1
    if speedright < -1:
        speedright = -1

    # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke   
    HBridge.setMotorLeft(speedleft)
    HBridge.setMotorRight(speedright)

    # Mit diesem Aufruf wird an die Web-Oberflaeche zurueck gegeben
    # welcher Button zuletzt gedrueckt wurde.
    ret_data = {"value": "Backward button pressed."}
    return jsonify(ret_data) 

# Die Funktion "ButtonTurnLeft()" legt fest, dass das Roboter  
# Auto nach links faehrt.
@app.route('/left/', methods=['GET'])
def ButtonTurnLeft():
    global speedleft
    global speedright

    speedright = speedright + step
    speedleft = speedleft - step

    # Die Geschwindigkeit darf nicht kleiner als -1 werden oder 
    # groesser als +1 werden da sonst jeweils die 100% 
    # ueberschritten waren.   
    if speedleft < -1:
        speedleft = -1
    if speedright > 1:
        speedright = 1

    # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke   
    HBridge.setMotorLeft(speedleft)
    HBridge.setMotorRight(speedright)

    # Mit diesem Aufruf wird an die Web-Oberflaeche zurueck gegeben
    # welcher Button zuletzt gedrueckt wurde.
    ret_data = {"value": "Left button pressed."}
    return jsonify(ret_data)

# Die Funktion "ButtonTurnRight()" legt fest, dass das Roboter  
# Auto nach rechts faehrt.
@app.route('/right/', methods=['GET'])
def ButtonTurnRight():   
    global speedleft
    global speedright

    speedright = speedright - step
    speedleft = speedleft + step

    # Die Geschwindigkeit darf nicht kleiner als -1 werden oder 
    # groesser als +1 werden.   
    if speedright < -1:
        speedright = -1
    if speedleft > 1:
        speedleft = 1

    # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke      
    HBridge.setMotorLeft(speedleft)
    HBridge.setMotorRight(speedright)

    # Mit diesem Aufruf wird an die Web-Oberflaeche zurueck gegeben
    # welcher Button zuletzt gedrueckt wurde.
    ret_data = {"value": "Right button pressed."}
    return jsonify(ret_data)  

# Die Funktion "ButtonStop()" legt fest, dass das Roboter
# Auto anhaelt.
@app.route('/stop/', methods=['GET'])
def ButtonStop():   
    global speedleft
    global speedright

    # Die Geschwindigkeit wird auf 0 gesetzt damit die Motoren 
    # stoppen
    speedleft = 0
    speedright = 0

    # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke
    HBridge.setMotorLeft(speedleft)
    HBridge.setMotorRight(speedright)

    # Mit diesem Aufruf wird an die Web-Oberflaeche zurueck gegeben
    # welcher Button zuletzt gedrueckt wurde.
    ret_data = {"value": "Stopp button pressed."}
    return jsonify(ret_data) 

# Die Funktion "status()" definiert die Meldungen die das 
# Roboter Auto an die Web-Oberflaeche zuerueck gibt.
# Hier waere es z. B. moeglich auch die gemessene Entfernung
# der Ultraschall-Sensoren oder die Sensorwerte des SenseHAT
# an die Web-Overflaeche weiter zu geben.
@app.route('/status/', methods=['GET'])
def status():
    global speedleft
    global speedright
    global error_msg

    display_speedl = round(speedleft,2)
    display_speedr = round(speedright,2)

    # Mit diesem Aufruf werden die Werte an die Web-Oberflaeche zurueck
    # gegeben, die z. B.  aktuell fuer die Motoren gesetzt sind.
    if error_msg == "":
        error_msg = ("No error!")
    ret_data = {"speedl": display_speedl, "speedr": display_speedr,
        "error_msg": error_msg}
    return jsonify(ret_data)

# Ruft die initiate Funktion auf um die initialen Variablen zu setzen.
initiate()   

# Hier wird der Flask Web-Server selbst gestartet mit dem Port 8181.
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8181, debug=False)
