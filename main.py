from machine import Pin, I2C
import ds1307
from time import localtime, mktime, sleep
import math

#rtc i2c pins
sda_pin = 26
scl_pin = 27

#pins for 7seg display
digits = (9, 8, 7, 6) #dig 1 2 3 4
segments = (11, 12, 16, 14, 17, 10, 13) # A B C D E F G, dp at Pin 15


#pins to activate relays
rel1 = 18
rel2 = 19
Pin(rel1, mode=Pin.OUT, value=0)
Pin(rel2, mode=Pin.OUT, value=0)

#segments values for displaying numbers  
num = {"-": (0,0,0,0,0,0,0),
       "0": (1,1,1,1,1,1,0),
       "1": (0,1,1,0,0,0,0),
       "2": (1,1,0,1,1,0,1),
       "3": (1,1,1,1,0,0,1),
       "4": (0,1,1,0,0,1,1),
       "5": (1,0,1,1,0,1,1),
       "6": (1,0,1,1,1,1,1),
       "7": (1,1,1,0,0,0,0),
       "8": (1,1,1,1,1,1,1),
       "9": (1,1,1,1,0,1,1)}

#rtc i2c setup
i2c = I2C(1, sda=Pin(sda_pin), scl=Pin(scl_pin))
ds = ds1307.DS1307(i2c)

def init():
    #initiate digit pins at HIGH
    for digit in digits:
        Pin(digit, Pin.OUT)
        Pin(digit).on()
    
    #initiate segment pins at LOW
    for seg in segments:
        Pin(digit, Pin.OUT)
        Pin(digit).off()
init()

deadline = (2022, 1, 2, 17, 41, 0, 0, 0)  #time to countdown to

while True:
    
    current = localtime() #current = ds.datetime() for RTC
    
    #time difference between the two events/moments in seconds
    diff = mktime(deadline) - mktime(current)
    
    #convert seconds to hours, minutes, seconds
    hours, minutes = divmod(diff,3600)
    minutes, seconds = divmod(minutes,60)
    seconds = math.trunc(seconds)
    
    #choosing between seconds countdown and HH:MM countdown
    if (hours == 0) and (minutes <=1):
        s = f"--{seconds:02d}" 
    else:
        s = f"{hours:02d}{minutes:02d}" 
    
    for digit in range(4):
        for seg in range(7):
            Pin(segments[seg], mode=Pin.OUT, value=num[str(s[digit])][seg])
        Pin(digits[digit], mode=Pin.OUT, value=0)
        sleep(0.001)
        Pin(digits[digit], mode=Pin.OUT, value=1)
    
    if s == "--00":
        Pin(rel1, mode=Pin.OUT, value=1)
        sleep(2)
        Pin(rel2, mode=Pin.OUT, value=1)
        quit
init()