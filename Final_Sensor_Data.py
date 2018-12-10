
from network import LoRa
import socket
import time
import _thread
import utime
from time import sleep
from machine import Pin, Timer
import machine

#Function created to calculate median throughout program
def calculate_median(l):
    l = sorted(l)
    l_len = len(l)
    if l_len < 1:
        return None
    if l_len % 2 == 0:
        return  (l[(l_len-1)//2] + l[(l_len+1)//2]) // 2
    else:
        return l[(l_len-1)//2]

#Function created to zero the sensor unit relative to location in pipe
def zeroDistance():
    echo = Pin(Pin.exp_board.G8, mode=Pin.IN)
    trigger = Pin(Pin.exp_board.G7, mode=Pin.OUT)
    trigger(0)
    chrono = Timer.Chrono()
    i = 0
    dist = 0
    while True:
        chrono.reset()
        trigger(1)
        time.sleep_us(10)
        trigger(0)
        while echo() == 0:
            pass
        chrono.start()
        while echo() == 1:
            pass
        chrono.stop()
        dist = chrono.read_us()/148.0
        i = i + 1
        if i == 10:
            i = 0
            zeroDist = dist
            break

        time.sleep_ms(80)
    return zeroDist

#Function created to collect water depth
def data_collector(zero_dist):
    echo = Pin(Pin.exp_board.G8, mode=Pin.IN)
    trigger = Pin(Pin.exp_board.G7, mode=Pin.OUT)
    trigger(0)
    chrono = Timer.Chrono()
    i = 0
    water_depth = []
    while True:
        chrono.reset()
        trigger(1)
        time.sleep_us(10)
        trigger(0)
        while echo() == 0:
            pass
        chrono.start()
        while echo() == 1:
            pass
        chrono.stop()
        distance = round(chrono.read_us() / 148.0,2)
        water_level = zero_dist - distance
        water_depth.insert(i,water_level)
        i = i + 1
        if i == 5:
            i = 0
            depth = calculate_median(water_depth)
            water_depth.clear()
            break
        time.sleep_ms(80)
    return depth

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# Main area where the code is running. This is where the data is gathered and sent to pybytes.
def send_env_data():
    # Setup up the LoRa communcation to be used in North America
    lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    idx = 0
    time.sleep(120)
    zero_distance_idx = 0

    # Determine the size of the pipe. Do this five different times to get the most accurate reading possible.
    while(zero_distance_idx < 5):
         zero_dist = zeroDistance() # This variable is determined by the size of the pipe
         print(zero_dist)
         time.sleep(5)
         zero_distance_idx = zero_distance_idx + 1


    # Take a reading inside the pipe once every minute for a total of 10 minutes and then enter into a deep sleep state to conserve power.
    while (True):
        while(idx < 10):
            data_to_send = data_collector(zero_dist) # Call the function that collects the sensor data
            data = str(data_to_send)
            print("Data sent")
            print(data)
            s.send(data)
            time.sleep(60)
            idx = idx + 1
        print("Entering Sleep")
        machine.deepsleep(300000)
        idx = 0




# Start the actual thread that is going to be used for all of the code.
_thread.start_new_thread(send_env_data, ())
