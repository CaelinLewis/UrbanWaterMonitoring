# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def water_level():
    # set Trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)

    # Allow module to settle
    time.sleep(0.5)
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    # Wait 10us
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # Calculate pulse length
    TimeElasped = StopTime - StartTime
    
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    temp = 21 # Temperature in degrees Celcius 
    speedSound = 33100 + (0.6*temp)
    distance = TimeElasped * speedSound
    
    # That was the distance there and back, so halve the value
    distance = distance / 2
    water_level = distance
    # Convert water level to in
    water_level = water_level* 0.393701

    return water_level

if __name__== '__main__':
    try:
        while True:
            dist = water_level()
            print ("Measured Distance = %.1f in" % dist)
            time.sleep(1)

        #Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
