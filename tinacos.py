import RPi.GPIO as GPIO
import mysql.connector
import socket
from datetime import datetime
import time, os
hostname = socket.gethostname()
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

seconds = time.time()
tinaco = 3

mydb = mysql.connector.connect(
        host = "192.168.1.105",
        user = "raspberry_user",
        passwd = "89288-a",
        database = "raspberry",
        )

my_cursor = mydb.cursor()

#from time import sleep
#Set DATA pin
TRIG = 6
ECHO = 13
ALARM = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

GPIO.setup(ALARM,GPIO.OUT)
GPIO.output(ALARM, True)

print ("Waiting For Sensor To Settle")
time.sleep(1) #settling time

def get_distance():
        dist_add = 0
        k=0
        for x in range(20):
                try:
                        GPIO.output(TRIG, True)
                        time.sleep(0.00001)
                        GPIO.output(TRIG, False)

                        while GPIO.input(ECHO)==0:
                                pulse_start = time.time()

                        while GPIO.input(ECHO)==1:
                                pulse_end = time.time()

                        pulse_duration = pulse_end - pulse_start

                        distance = pulse_duration * 17150

                        distance = round(distance, 3)
                        print (x, "distance: ", distance)

                        if(distance > 125):# ignore erroneous readings (max distance cannot be more than 125)
                                k=k+1
                                continue

                        dist_add = dist_add + distance
                        #print "dist_add: ", dist_add
                        time.sleep(.1) # 100ms interval between readings

                except Exception as e:

                        pass


        print ("x: ", x+1)
        print ("k: ", k)

        avg_dist=dist_add/(x+1 -k)
        dist=round(avg_dist,3)
        #print ("dist: ", dist)
        return dist

def insert_data(dist):
   sql = "INSERT INTO tinacos (tinaco, nivel, timestamp, date_time) VALUES(%s,%s,%s,%s)"
   values = (tinaco, dist, seconds, formatted_date)
   my_cursor.execute(sql,values)
   mydb.commit()


def low_level_warning(dist):
        level=114-dist
        if(level<40):
                print("level low : ", level)
                GPIO.output(ALARM, False)
        else:
                GPIO.output(ALARM, True)
                print("level ok")

distance=get_distance()
insert_data(distance)
print ("distance: ", distance)
low_level_warning(distance)
GPIO.cleanup()
print ("---------------------")

