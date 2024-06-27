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
passed_time = 600 # 3 minutes

urls = [
    "http://192.168.0.100",
    "http://192.168.0.101",
    "http://192.168.0.102",
    "http://192.168.0.103",
    "http://192.168.0.104",
    "http://192.168.0.105",
    "http://192.168.0.106",
    "http://192.168.0.107"
]

# Ball states
ball_go = "on"
ball_stop = "off"

async def make_request(url, state):
    request_url = f"{url}/{state}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as resp:
                print(f"{request_url} Response: {resp.status}")
    except aiohttp.ClientError as e:
        print(f"Failed to connect to {request_url}: {e}")

async def handle_requests(state):
    tasks = [make_request(url, state) for url in urls]
    await asyncio.gather(*tasks)

async def measure_distance():
    global out_of_range_time

    while True:
        GPIO.output(TRIG, False)
        print ("Waiting For Sensor To Settle")
        time.sleep(2)

        # Send a pulse to the TRIG pin
        GPIO.output(TRIG, True)
        await asyncio.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Measure the time for the pulse to return
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        # Calculate distance based on pulse duration
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        # Print the calculated distance
        print("Distance: ", distance - 0.5, "cm")

        if 20< distance < 400:
            print ("Distance: ",distance - 0.5, "cm")
            # request balls to move
            # Send the HTTP request
            await handle_requests(ball_go)
            out_of_range_time = None # Reset the out of range time
        else:
            print ("Out of Range") # display out of range
            if out_of_range_time is None:
                out_of_range_time = time.time() # Record the time when it went out of range
            elif time.time() - out_of_range_time >= passed_time:
                # Send the HTTP request to balls to stop
                await handle_requests(ball_stop)
                out_of_range_time = time.time()

# Clean up GPIO settings on exit
def cleanup_gpio():
    GPIO.cleanup()

# Create an event loop and run the measure_distance coroutine
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(measure_distance())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()