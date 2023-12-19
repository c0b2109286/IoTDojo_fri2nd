import _peripheral
import _central
from machine import I2C,Pin
from vl53l1x import VL53L1X
import machine

red_pin = 13
red_led = machine.Pin(red_pin, machine.Pin.OUT)
green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
blue_pin = 15
blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

class ManegementCondition():
    def _CheckConditionTo(self, fn, distance, blue_led, mode, time): #senserへ経路構築の開始を伝える
        _peripheral.periph(fn, distance, blue_led, mode, time)
        
    def _CheckConditionFrom(self, fn, blue_led, mode): #senserから距離送信の開始を受け取る
        _central.centr(fn, blue_led, mode)
        
def MGCondition(fn, Pmode_change, Cmode_change, condition):
    
    distance = "10"
    timeout = 10
    
    mg = ManegementCondition()
    
    #経路構築開始を受け取る
    if condition is 0:
        #Cmode:1
        mg._CheckConditionFrom(fn, blue_led, Cmode_change) #Cmode:1
        
        Cmode_change += 1
    
    #センサーデータ開始を伝える
    if condition is 1:
        mg._CheckConditionTo(fn, distance, blue_led, Pmode_change, timeout) #P2
        
        Pmode_change += 1
    
    # condition 0 / Pmode:1, Cmode:2
    # condition 1 / Pmode:3, Cmode:3
    print(Pmode_change)
    print(Cmode_change)
    return Pmode_change, Cmode_change
    
if __name__ == "__main__":
    Pmode_change = 1
    Cmode_change = 1
    fn = 'info/SN02.json'
    condition = 0
    MGCondition(fn, Pmode_change, Cmode_change, condition)
