
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location
# and other details.
import time
import board
import busio
import asyncio
# import adafruit_gps
from disp4x14 import disp4x14
from adafruit_ht16k33 import segments


from test_machine import TestMachine   
from bus_master import BusMaster
import data

uart_radio = busio.UART(board.D5, board.D6, baudrate=9600)
uart_bt = busio.UART(board.D12, board.D11, baudrate=9600)

#from log import log

#display = segments.Seg14x4(board.I2C())  # uses board.SCL and board.SDA
# i2c = board.I2C()  # uses board.SCL and board.SDA
# Create a second UART on alternate pins (example: GPIO 5 and 6)

bus_master = BusMaster(uart_radio)
tm = TestMachine(bus_master)
parsed_msg = {}

#display.marquee("T2503 LoRa Test Central Master", loop=False)

def parse_cmd(str): 
    lst = str.split(',')
    # <','B','R', '3', 'P', '20', 'N', '345', 'T', '-99','S', '-68', '>', '\n']
    #print(lst)
    if (lst[0] == data.RADIO_MSG_START and 
        lst[1] == 'B' and 
        lst[2] == 'R' and 
        lst[4] == 'P' and 
        lst[6] == 'N' and
        lst[8] == 'S' and 
        lst[10] == 'T' and
        lst[12] == data.RADIO_MSG_END):  
        cmd = {'msg_type':lst[1] ,
               'radio': int(lst[3]), 
               'pwr': int(lst[5]), 
               'nbr': int(lst[7]), 
               'base_rssi': int(lst[9]),
               'remote_rssi': int(lst[11])}
        return cmd
    else:
        return None


async def bus_cmd():
    global parsed_msg
    state = 0
    while True:
        if state == 0:
            bus_master.set_base_node()
            await asyncio.sleep(1.0)
            state = 5
        if state == 5:    
            rxstr = bus_master.receive()  
            if (rxstr is not None):
                rxstr = rxstr.rstrip()  
                print(rxstr)
                parsed_msg = parse_cmd(rxstr)
                if parsed_msg is not None: 
                    state = 10
                    await asyncio.sleep(1.0) 
                else:
                    await asyncio.sleep(0.1)    
        elif state == 10:
                print("Received message: ", parsed_msg)
                disp4x14.new_msg(parsed_msg)
                await asyncio.sleep(1.0)
                bus_master.ack_msg(parsed_msg)
                state = 20
                await asyncio.sleep(2.0)
        elif state == 20:
                bus_master.log_msg(parsed_msg)
                state = 0
                await asyncio.sleep(1.0)



async def task_display4x14():
    while True:
        disp4x14.run()
        await asyncio.sleep(1.0)

async def test_machine():
    while True:
        #uart_radio.write(b"Hello from radio UART!")
        #uart_bt.write(b"Hello from bluetooth UART!")
        sleep_sec = tm.state_machine() 
        await asyncio.sleep(sleep_sec)

async def main():
    bus_cmd_task = asyncio.create_task(bus_cmd())
    disp4x14_task = asyncio.create_task(task_display4x14()) 
    # test_task = asyncio.create_task(test_machine())

    await asyncio.gather(bus_cmd_task, disp4x14_task)  
    print("done")

asyncio.run(main())

     