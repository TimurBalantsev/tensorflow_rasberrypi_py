from gpiozero import DistanceSensor
from time import sleep
import adafruit_dht
import psutil
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()


sensorDis = DistanceSensor(23, 18)
sensorHum = adafruit_dht.DHT11(16)
humidity = None
temp = None
    

def get_distance():
    return sensorDis.distance

def get_humidity():
    try:
        return sensorHum.humidity
    except RuntimeError as error:
        return None
    
def get_temperature():
    try:
        return sensorHum.temperature
    except RuntimeError as error:
        return None

if __name__ == "__main__":
    while True:
        try:
            temp = sensorHum.temperature
            humidity = sensorHum.humidity
        except RuntimeError as error:
            continue
        print('Distance to nearest object is', sensorDis.distance, 'm', '\nHumidity : ', humidity, ' ', temp)
        sleep(0.1)