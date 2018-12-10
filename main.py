<<<<<<< HEAD
from network import LoRa
import socket
import time
=======

from network import LoRa
import socket
import time
import _thread
import utime
from time import sleep
from machine import Pin, Timer
import machine

# Increment index used to scan each point from vector sensors_data
def inc(index, number):
    if index < number-1:
        return index+1
    else:
        return 0


def calculate_median(l):
    l = sorted(l)
    l_len = len(l)
    if l_len < 1:
        return None
    if l_len % 2 == 0:
        return  (l[(l_len-1)//2] + l[(l_len+1)//2]) // 2
    else:
        return l[(l_len-1)//2]


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
        if i == 13:
            i = 0
            depth = calculate_median(water_depth)
            water_depth.clear()
            break
        time.sleep_ms(80)
    return depth
>>>>>>> 61dd784c7d0ca1cdb4ecdd6f15d2cd92858cd3c5

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
<<<<<<< HEAD
lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

while True:
        data = s.recv(64)
        print(data)
        time.sleep(5)
=======
# Main area where the code is running. This is where the data is gathered and sent to pybytes.
def send_env_data():
    # Setup up the LoRa communcation to be used in North America
    lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    idx = 0
    zero_dist = 11.12 # This variable is determined by the size of the pipe

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
>>>>>>> 61dd784c7d0ca1cdb4ecdd6f15d2cd92858cd3c5
