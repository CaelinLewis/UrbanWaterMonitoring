import time
from machine import Pin, Timer

def data_collector(zero_dist):
    echo = Pin(Pin.exp_board.G8, mode=Pin.IN)
    trigger = Pin(Pin.exp_board.G7, mode=Pin.OUT)

    trigger(0)

    chrono = Timer.Chrono()

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
    water_level = round(zero_dist - distance,2)


    return water_level
