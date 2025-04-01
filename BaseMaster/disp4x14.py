from adafruit_ht16k33 import segments
import neopixel
import board
import busio    
import asyncio
import time 
import data

class display4x14:
    def __init__(self):
        self.msg = None
        self.pos = 0
        self.state = 0
        self.display = segments.Seg14x4(board.I2C())  # uses board.SCL and board.SDA
        self.display.marquee("T2503 LoRa Test Central Master", loop=False)
        self.rgb = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.rgb.brightness = 0.1   

    
    def new_msg(self, msg):
        self.msg = msg
        #"{} {}dB #{} RSSI{}".format(
        #                    data.radio_labels[msg['radio']], 
        #                    msg['pwr'], 
        #                    msg['nbr'], 
        #                    msg['rssi'])
        #self.pos = 0

               
    def run(self):
        if self.state == 0:
            if self.msg is not None:
                self.rgb[0] = data.rgb_colors[self.msg['radio']]
                self.state = 10
        if self.state == 10:
            buf4 = data.radio_labels[self.msg['radio']]
            self.state = 11
        elif self.state == 11:
            buf4 = "P{}".format(self.msg['pwr'])
            self.state = 12 
        elif self.state == 12: 
            buf4 = "n{}".format(self.msg['nbr'])
            self.state = 13
        elif self.state == 13:
            buf4 = "{}".format(self.msg['remote_rssi'])
            self.state = 0
        if self.msg is not None:
            self.display.fill(0)     
            self.display.print(buf4)
            self.display.show()

disp4x14 = display4x14()