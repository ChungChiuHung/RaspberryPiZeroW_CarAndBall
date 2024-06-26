import RPi.GPIO as GPIO # Import GPIO library
import time # Import time library
import aiohttp # Import aiohttp library
import asyncio # Import asyncio library

print("aiohttp version: ", aiohttp.__version__)

GPIO.setmode(GPIO.BCM) # Set GPIO pi number

TRIG = 15 # Associate pin 15 to TRIG
ECHO = 14 # Associate pin 14 to Echo

print ("Distance measurement in progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

out_of_range_time = None
passed_time = 180 # 10 minutes

urls = [
    "http://192.168.1.11",
    "http://192.168.1.12",
    "http://192.168.1.13",
    "http://192.168.1.14",
    "http://192.168.1.15",
    "http://192.168.1.16",
    "http://192.168.1.17",
    "http://192.168.1.18"
]

ball_go = "on"
ball_stop = "off"

async def make_request(url, state):
    request_url = f"{url}/{state}"
    async with aiohttp.ClientSession() as session:
        async with session.get(request_url) as resp:
            print(f"{request_url} Response: {resp.status}")

async def handle_requests(state):
    tasks = [make_request(url, state) for url in urls]
    await asyncio.gather(*tasks)

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
        asyncio.run(handle_requests(ball_go))
        out_of_range_time = None # Reset the out of range time
    else:
        print ("Out of Range") # display out of range
        if out_of_range_time is None:
            out_of_range_time = time.time() # Record the time when it went out of range
        elif time.time() - out_of_range_time >= passed_time:
            # Send the HTTP request to balls to stop
            asyncio.run(handle_requests(ball_stop))
            out_of_range_time = time.time()