import RPi.GPIO as GPIO
import time
import sqlite3
GPIO.setmode(GPIO.BCM)

TRIG = 15
ECHO = 14

print ("Distance measurement in progress")

GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print ("Waiting For Sensor To Settle")
time.sleep(5)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0:
    pulse_start = time.time()

while GPIO.input(ECHO)==1:
    pulse_end = time.time()

pulse_duration = pulse_end = pulse_start

distance = pulse_duration * 17150
distance = round(distance, 2)

if distance > 2 and distance < 400:
    print ("Distance: ",distance - 0.5, "cm")
else:
    print ("Out of Range")

#Get the time in the right format
dtg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+".000"
print("Local current time:", dtg)

try:
    #opens a file called measurments
    db = sqlite3.connect('home/pi/measurements')
    # Get a cursor object
    cursor = db.cursor()
    #Insers the values into the table
    cursor.execute('''INSERT INTO distance(dtg, ultrasonic)
                   VALUES(?,?)''', (dtg,distance))
    # Commit the change
    db.commit()
except Exception as e:
    db.rollback()
    raise e
finally:
    db.close()