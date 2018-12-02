import time
from machine import Pin, Timer
from Distance import calculate_median

def zeroDistance():
    echo = Pin(Pin.exp_board.G8, mode=Pin.IN)
    trigger = Pin(Pin.exp_board.G7, mode=Pin.OUT)
    trigger(0)
    chrono = Timer.Chrono()
    i = 0
    dist = []

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

        dist = insert(i,chrono.read_us()/148.0)
        i = i + 1
        if i == 10:
            i = 0
            zeroDist = calculate_median(dist)
            dist.clear()
            break

        time.sleep_ms(80)

    return zeroDist
