import _peripheral
import _central
from machine import I2C,Pin
#from vl53l1x import VL53L1X
import machine

red_pin = 13
red_led = machine.Pin(red_pin, machine.Pin.OUT)
green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
blue_pin = 15
blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

fn = 'info/DN02.json'

class ManagementDist():
    # センサデバイスの行う動作を纏めたクラス.
    # Manegmentクラスを定義して経路データの送受信と書き込み(，確認)を行う各モジュールを呼び出すdef関数を定義する．
    def SenserdataCatch(self, fn, green_led, mode):
        Dist = _central.centr(fn, green_led, mode)
        return Dist
        
    def SenserdataSend(self, fn, distance, green_led, mode,time): # 作成した経路表に基づく距離データの送信
        _peripheral.periph(fn, distance, green_led, mode, time)
    
def MGDist(fn, Pmode_change,Cmode_change):
    mg = ManagementDist()
    fn = 'info/DN02.json'
    #distance = mg.SenserdataCatch(fn, green_led, Cmode_change)
    distance = mg.SenserdataCatch(fn, red_led, Cmode_change)
    if distance is not None:
        mg.SenserdataSend(fn, distance, green_led, Pmode_change, time=20)

if __name__ == "__main__":
    Pmode_change = 2
    Cmode_change = 2
    fn = 'info/DN02.json' 
    MGDist(fn, Pmode_change, Cmode_change)
