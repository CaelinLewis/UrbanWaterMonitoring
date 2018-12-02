# Import what is necessary to create a thread
import _thread
from time import sleep
from network import LoRa
import socket


​# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

# Define your thread's behaviour, here it's a loop sending sensors data every 10 seconds
def send_env_data():
    while (pybytes):
        if(s.recv(64)):
            data_to_send_to_pybytes = float(s.recv(64).decode())
            pybytes.send_virtual_pin_value(False, 1,data_to_send_to_pybytes )
        sleep(60)
​
# Start your
_thread.start_new_thread(send_env_data, ())
