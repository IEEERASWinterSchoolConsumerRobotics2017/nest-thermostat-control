import nest
import os
import sys
import socket
import threading
import math

nestUsername = "foo"
nestPassword = "bar"
ip = '10.18.81.7'
port = 8893
buffSize = 1024
target = 0 # in celcius
actual = 0 # in celcius
napi = None



def main():
    global nestUsername
    global nestPassword
    global target
    global actual
    global napi

    if 'USERNAME' in os.environ and 'PASSWORD' in os.environ:
        nestUsername = os.environ['USERNAME']
        nestPassword = os.environ['PASSWORD']
    else:
        print("Please set environment variables USERNAME and PASSWORD")
        sys.exit()
    print("Starting to collect current temperatures")
    napi = nest.Nest(nestUsername, nestPassword)
    getCurrentTemps()
    print("Current temperature collected")
    if(target != 0 and actual != 0):
        print("Got valid values")
    programLoop()

def programLoop():
    global target
    global actual
    threading.Timer(30.0, programLoop).start()

    print("checking server for updates")
    oldTarget = target
    getTempsFromServer()
    if(oldTarget != target):
        print("Updating nest to new temperature, Expected: " + str(oldTarget) + ", Got: " + str(target))
        setTargetNest(target)

    oldTemperature = math.ceil(actual)
    print("checking nest for updates")
    getCurrentTemps()
    if(oldTemperature != actual):
        print("Updating server to new temperature")
        setActualServer(actual)
    print("Sleeping")
    print()
    print()


def getCurrentTemps():
    global nestUsername
    global nestPassword
    global target
    global actual
    global napi

    target = napi.devices[0].target
    print('Target (F): ' + str(nest.utils.c_to_f(target)))
    actual = napi.devices[0].temperature
    print('Actual (F): ' + str(nest.utils.c_to_f(actual)))

#in Celcius
def setTargetNest(targetTemp):
    global nestUsername
    global nestPassword
    global napi

    for device in napi.devices:
        device.target = int(targetTemp)
    print("nest Changed to " + str(targetTemp))

def getTempsFromServer():
    global target
    global actual
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    message = b"req thermostat all"
    try:
        s.send(message)
        data = s.recv(256)
        parsed = data.split( )
        print(parsed)
        target = int(round(nest.utils.f_to_c(float(parsed[3]))))
        actual = int(round(nest.utils.f_to_c(float(parsed[4]))))
    finally:
        s.close();

#in Celcius
def setActualServer(actualTemp):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    message = b"set thermostat actual %f" % nest.utils.c_to_f(actualTemp)
    try:
        s.send(message)
        data = s.recv(256)
        print(data)
        if(data != "rep ok"):
            print("Problem Updating the server with actual temperature")
        #process response here
    finally:
        s.close();

#in celsius
def setTargetServer(targetTemp):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    message = b"set thermostat des tmp %f" % nest.utils.c_to_f(targetTemp)
    try:
        s.send(message)
        data = s.recv(256)
        print(data)
        if(data != "rep ok"):
            print("Problem Updating the server's target temperature")
        #process response here
    finally:
        s.close();

##########################################################

if __name__ == "__main__":
    main()
