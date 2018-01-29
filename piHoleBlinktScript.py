import blinkt
import time

from blinkt import set_brightness, set_pixel, show, clear

blinkt.set_clear_on_exit()

def watch(fn, words):
    fp = open(fn, 'r')
    fp.seek(0, 2)
    while True:
        new = fp.readline()
        # Once all lines are read this just returns ''
        # until the file changes and a new line appears

        if new:
            for word in words:
                if word in new:
                    fp.seek(0, 2)
                    yield (word, new)
        else:
            time.sleep(0.5)

fn = '/var/log/pihole.log'
words = ['/etc/pihole/gravity.list']


set_brightness(0.1)

for hit_word, hit_sentence in watch(fn, words):
    for index in range(8):
        set_pixel(index, 255, 0, 255)
        if index != 0:
            set_pixel(index - 1, 0, 0, 0)
        show()
        time.sleep(.005)
        if index == 7:
            set_pixel(index, 0, 0, 0)
            show()
