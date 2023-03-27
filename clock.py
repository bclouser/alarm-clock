import board
import pygame
from adafruit_ht16k33.segments import Seg7x4

i2c = board.I2C()
display = Seg7x4(i2c)

display.brightness = 0.5
#display.blink_rate = 3

display.print("AbCd")
display.print("12:43")



pygame.mixer.init()
pygame.mixer.music.load("testFile.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
        continue



