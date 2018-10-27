import time
from machine import Pin, Timer

def data_collector(zero_dist):
    echo = Pin(Pin.exp_board.G8, mode=Pin.IN)
    trigger = Pin(Pin.exp_board.G7, mode=Pin.OUT)

    trigger(0)

    chrono = Timer.Chrono()

    i = 0
    k = 0
    water_depth = []
    depth = []
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
        water_level = round(zero_dist - distance,2)
        water_depth.insert(i,water_level)


        i = i + 1
        if i == 270:
            i = 0
            if k < 25:
                depth_cal = round(sum(water_depth)/len(water_depth),2)
                depth.insert(k,depth_cal)
                k = k + 1
                water_depth.clear()
            else:
                break

        time.sleep_ms(80)
    return depth
