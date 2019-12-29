import time
import http.client, urllib
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)
chan3 = AnalogIn(ads, ADS.P2)
tinaco1 = -10.442 + 80.321 * chan1.voltage
tinaco2 = -23.588 + 70.621 * chan2.voltage
tinaco3 = -131.579 + 263.158 * chan3.voltage

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

def write_thingspeak(v1, tinaco1, v2, tinaco2, v3, tinaco3):
        params = urllib.parse.urlencode({'field1': v1, 'field2': tinaco1, 'field3': v2, 'field4': tinaco2, 'field5': v3, 'field6': tinaco3,   'key':'001WB3XH5F34A84Z'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print (response.status, response.reason)
        data = response.read()
        conn.close()

#while True:
#    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
#    time.sleep(0.5)
print("{:>5.3f}\t{:>5.3f}\t{:>5.3f}\t{:>5.3f}\t{:>5.3f}\t{:>5.3f}".format(chan1.voltage, tinaco1,chan2.voltage,tinaco2, chan3.voltage, tinaco3))
write_thingspeak(round(chan1.voltage,2),round(tinaco1,2),round(chan2.voltage,2),round(tinaco2,2),round(chan3.voltage,2),round(tinaco3,2))
