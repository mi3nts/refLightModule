import time
import board
import adafruit_ltr390

i2c = board.I2C()
ltr = adafruit_ltr390.LTR390(i2c)

while True:
    print("UV:", ltr.uvs, "\t\tAmbient Light:", ltr.light)
    time.sleep(1.0)

