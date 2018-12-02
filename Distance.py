import time
from machine import Pin, Timer
import zeroDistance



def calculate_median(l):
    l = sorted(l)
    l_len = len(l)
    if l_len < 1:
        return None
    if l_len % 2 == 0:
        return  (l[(l_len-1)//2] + l[(l_len+1)//2]) // 2
    else:
        return l[(l_len-1)//2]

zero_dist = zeroDistance()

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
