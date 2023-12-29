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

class ManegementCondition():
    def _CheckConditionTo(self, fn, distance, blue_led, mode, time): #senserへ経路構築の開始を伝える
        _peripheral.periph(fn, distance, blue_led, mode, time)
        
        
    def _CheckConditionFrom(self, fn, blue_led, mode):#senserから距離送信の開始を受け取る
        data = _central.centr(fn, blue_led, mode)
        return data
        
def MGCondition(fn, Pmode_change, Cmode_change, condition):
    
    data = "call_senser2"
    timeout = 10
    
    mg = ManegementCondition()
    
    #経路構築開始　（P:2,C,2）
    if condition is 0:
        rdata = mg._CheckConditionFrom(fn, blue_led, Cmode_change)
        Cmode_change += 1
        
        mg._CheckConditionTo(fn, rdata, blue_led, Pmode_change, timeout)
        Pmode_change += 1
        
    #距離開始（P:5,C:5）
    if condition is 1:
        mg._CheckConditionTo(fn, data, blue_led, Pmode_change, timeout)
        Pmode_change += 1
        
        mg._CheckConditionFrom(fn, blue_led, Cmode_change)
        Cmode_change += 1
    
    print(Pmode_change)
    print(Cmode_change)
    return Pmode_change, Cmode_change
    
if __name__ == "__main__":
    Pmode_change = 2
    Cmode_change = 2
    condition = 0
    fn = 'info/DN05.json'
    MGCondition(fn, Pmode_change, Cmode_change, condition)
