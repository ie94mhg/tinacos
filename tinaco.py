import RPi.GPIO as GPIO
import time
import sys
import httplib, urllib
from time import localtime, strftime

def write_thingspeak(tinaco1, tinaco2):
#def write_thingspeak(tinaco1):
        params = urllib.urlencode({'field1': tinaco1, 'field2': tinaco2,   'key':'VLHH3J2LW3XCBNRL'})
        #params = urllib.urlencode({'field1': tinaco1,    'key':'VLHH3J2LW3XCBNRL'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()

if len(sys.argv) == 5:
        GPIO_TRIGGER1 = int(sys.argv[1])
        GPIO_ECHO1 = int(sys.argv[2])
        GPIO_TRIGGER2 = int(sys.argv[3])
        GPIO_ECHO2 = int(sys.argv[4])
else:
        print 'usage: sudo ./tinaco.py [GPIO_TRIGGER1|GPIO_ECHO1|GPIO_TRIGGER2|GPIO_ECHO2] GPIOpin#'
        print 'example: sudo ./tinaco.py 17 27 23 24'
        sys.exit(1)

GPIO.setmode(GPIO.BCM)     #Ponemos la placa en modo BCM
altura1=150
altura2=150
offset1=25
offset2=25
GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)  #Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO1,GPIO.IN)      #Configuramos Echo como entrada

GPIO.output(GPIO_TRIGGER1,False)    #Ponemos el pin 25 como LOW

#Obtenemos medicion del Tinaco #1
GPIO.output(GPIO_TRIGGER1,True)   #Enviamos un pulso de ultrasonidos
time.sleep(0.00001)              #Una pequea pausa
GPIO.output(GPIO_TRIGGER1,False)  #Apagamos el pulso
start1 = time.time()              #Guarda el tiempo actual mediante time.time()
while GPIO.input(GPIO_ECHO1)==0:  #Mientras el sensor no reciba senal...
    start1 = time.time()          #Mantenemos el tiempo actual mediante time.time()
while GPIO.input(GPIO_ECHO1)==1:  #Si el sensor recibe senal...
    stop1 = time.time()           #Guarda el tiempo actual mediante time.time() en otra variable
elapsed1 = stop1-start1             #Obtenemos el tiempo transcurrido entre envio y recepcion
distance1 = round((elapsed1 * 34300)/2,2)   #Distancia es igual a tiempo por velocidad partido por 2   D = (T x V)/2
tinaco1 = round(((altura1-distance1)*100)/(altura1-offset1),2)
print "Distancia:",distance1,"cm"                   #Devolvemos la distancia (en centimetros) por pantalla
print "Tanque al: ",tinaco1,"%"
time.sleep(1)                    #Pequena pausa para no saturar el procesador de la Raspberry

GPIO.cleanup()                       #Limpiamos los pines GPIO y salimos
#Obtenemos medicion del Tinaco #2
GPIO.setmode(GPIO.BCM)     #Ponemos la placa en modo BCM
GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)  #Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO2,GPIO.IN)      #Configuramos Echo como entrada
GPIO.output(GPIO_TRIGGER2,False)    #Ponemos el pin 25 como LOW
GPIO.output(GPIO_TRIGGER2,True)   #Enviamos un pulso de ultrasonidos
time.sleep(0.00001)              #Una pequea pausa
GPIO.output(GPIO_TRIGGER2,False)  #Apagamos el pulso
start2 = time.time()              #Guarda el tiempo actual mediante time.time()
while GPIO.input(GPIO_ECHO2)==0:  #Mientras el sensor no reciba senal...
    start2 = time.time()          #Mantenemos el tiempo actual mediante time.time()
while GPIO.input(GPIO_ECHO2)==1:  #Si el sensor recibe senal...
    stop2 = time.time()           #Guarda el tiempo actual mediante time.time() en otra variable
elapsed2 = stop2-start2             #Obtenemos el tiempo transcurrido entre envio y recepcion
distance2 = round((elapsed2 * 34300)/2,2)   #Distancia es igual a tiempo por velocidad partido por 2   D = (T x V)/2
tinaco2 = round(((altura2-distance2)*100)/(altura2-offset2),2)
print "Distancia:",distance2,"cm"                   #Devolvemos la distancia (en centimetros) por pantalla
print "Tanque al: ",tinaco2,"%"
GPIO.cleanup()                       #Limpiamos los pines GPIO y salimos

if tinaco1 is not None and tinaco2 is not None and tinaco1 > 0 and tinaco2 > 0:
        print 'tanque1={0:0.1f}%  tanque2={1:0.1f}%'.format(tinaco1, tinaco2)
#        print 'tanque1={0:0.1f}%'.format(tinaco1)
        write_thingspeak(tinaco1,tinaco2)
else:
        print 'Failed to get reading. Try again!'
        sys.exit(1)

