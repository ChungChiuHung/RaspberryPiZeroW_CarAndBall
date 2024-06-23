import RPi.GPIO as GPIO # Import GPIO library
import time # Import time library
import aiohttp # Import aiohttp library
import asyncio # Import asyncio library

GPIO.setmode(GPIO.BCM) # Set GPIO pi number

TRIG = 15 # Associate pin 15 to TRIG
ECHO = 14 # Associate pin 14 to Echo

print ("Distance measurement in progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

out_of_range_time = None
passed_time = 600 # 10 minutes

url_ball_1 = "http://192.168.1.11"
url_ball_2 = "http://192.168.1.12"
url_ball_3 = "http://192.168.1.13"
url_ball_4 = "http://192.168.1.14"
url_ball_5 = "http://192.168.1.15"
url_ball_6 = "http://192.168.1.16"
url_ball_7 = "http://192.168.1.17"
url_ball_8 = "http://192.168.1.18"

ball_go = "on"
ball_stop = "off"

async def make_request(url, state):
    request_url = f"{url}/{state}"
    async with aiohttp.ClientSession() as session:
        async with session.get(request_url) as resp:
            print(f"{request_url} Response: {resp.status}")

while True:
    GPIO.output(TRIG, False)
    print ("Waiting For Sensor To Settle")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if 20< distance < 480:
        print ("Distance: ",distance - 0.5, "cm")
        # request balls to move
        # Send the HTTP request
        asyncio.run(make_request(url_ball_1, ball_go))
        asyncio.run(make_request(url_ball_2, ball_go))
        asyncio.run(make_request(url_ball_3, ball_go))
        asyncio.run(make_request(url_ball_4, ball_go))
        asyncio.run(make_request(url_ball_5, ball_go))
        asyncio.run(make_request(url_ball_6, ball_go))
        asyncio.run(make_request(url_ball_7, ball_go))
        asyncio.run(make_request(url_ball_8, ball_go))

        out_of_range_time = None # Reset the out of range time
    else:
        print ("Out of Range") # display out of range
        if out_of_range_time is None:
            out_of_range_time = time.time() # Record the time when it went out of range
        elif time.time() - out_of_range_time >= passed_time:
            # Send the HTTP request to balls to stop
            asyncio.run(make_request(url_ball_1, ball_stop))
            asyncio.run(make_request(url_ball_2, ball_stop))
            asyncio.run(make_request(url_ball_3, ball_stop))
            asyncio.run(make_request(url_ball_4, ball_stop))
            asyncio.run(make_request(url_ball_5, ball_stop))
            asyncio.run(make_request(url_ball_6, ball_stop))
            asyncio.run(make_request(url_ball_7, ball_stop))
            asyncio.run(make_request(url_ball_8, ball_stop))

            out_of_range_time = time.time()