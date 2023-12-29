import _peripheral
import _central
from machine import I2C,Pin
import machine

red_pin = 13
red_led = machine.Pin(red_pin, machine.Pin.OUT)
green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
blue_pin = 15
blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

fn = 'info/DN02.json'

# a class that collects actions related to senser data
class ManagementDist():
    # receive senser data
    def SenserdataCatch(self, fn, green_led, mode):
        Dist = _central.centr(fn, green_led, mode)
        return Dist
    # send distance data based on the created route table
    def SenserdataSend(self, fn, distance, green_led, mode,time): 
        _peripheral.periph(fn, distance, green_led, mode, time)
    
def MGDist(fn, Pmode_change,Cmode_change):
    mg = ManagementDist()
    fn = 'info/DN02.json'
    distance = mg.SenserdataCatch(fn, red_led, Cmode_change)
    if distance is not None:
        mg.SenserdataSend(fn, distance, green_led, Pmode_change, time=20)

if __name__ == "__main__":
    Pmode_change = 2
    Cmode_change = 2
    fn = 'info/DN02.json' 
    MGDist(fn, Pmode_change, Cmode_change)
