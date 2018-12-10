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
# Set up the LoRa communication to receive the message from the device inside the pipe.
lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

# Checks to see if it receives any information from the device that is inside the pipe.
# If there is any information then immediately send that informatoin to Pybytes.
def send_env_data():
    while (pybytes):
        if(s.recv(64)):
            print(s.recv(64)) 
            print(type(s.recv(64)))
            data_to_send_to_pybytes = s.recv(64).decode()
            final_data_to_send_to_pybytes = str(data_to_send_to_pybytes)
            pybytes.send_virtual_pin_value(False, 1,final_data_to_send_to_pybytes )
        sleep(60)
​
# Thread
_thread.start_new_thread(send_env_data, ())
