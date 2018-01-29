# this script lights up your blinkt whenever pihole blocks an ad

import blinkt
import time

from blinkt import set_brightness, set_pixel, show, clear, NUM_PIXELS

blinkt.set_clear_on_exit()

def watch(fn, words):
    # open the log
    fp = open(fn, 'r')
    # go to the end of the log
    fp.seek(0, 2)
    while True:
        # get line
        new = fp.readline()
        # Once all lines are read this just returns ''
        # until the file changes and a new line appears

        if new:
            for word in words:
                if word in new:
                    # if new log entry for a blocked ad is found move to the end to avoid buildup of animation
                    fp.seek(0, 2)
                    # yield the hit
                    yield (word, new)
        else:
            time.sleep(0.5)

# set file path for pihole log and search term (this should work by default)
fn = '/var/log/pihole.log'
words = ['/etc/pihole/gravity.list'] # this is loged each time pi hole blocks an ad


set_brightness(0.1)

# for each time watch hits the search term
for hit_word, hit_sentence in watch(fn, words):
    # for each LED
    for index in range(NUM_PIXELS):
        # set color to purple
        set_pixel(index, 255, 0, 255)
        # turn off the preceding LED
        if index != 0:
            set_pixel(index - 1, 0, 0, 0)
        show()
        time.sleep(.005)
        # turn off the last pixel
        clear()
        show()
