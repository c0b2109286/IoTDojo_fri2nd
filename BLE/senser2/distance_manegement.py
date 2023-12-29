#import senddistance_peripheral
import _peripheral
import time
from machine import I2C,Pin
from vl53l1x import VL53L1X
import machine

red_pin = 13
red_led = machine.Pin(red_pin, machine.Pin.OUT)
green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
blue_pin = 15
blue_led = machine.Pin(blue_pin, machine.Pin.OUT)


class ManegementDist():
    def getdistance(self): # 距離データの取得
        I2C_SCL_PIN = 22  
        I2C_SDA_PIN = 21
        i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))

        distance = VL53L1X(i2c)
        count = 0 #count 変数を定義して初期値を0に設定する．

        # count が0の場合、距離センサーから距離データを読み取り，その後、1秒待機する．
        distance = distance.read()
        time.sleep_ms(1000)
        count += 1
        # 距離データを出力し、その値を返す．
        print("range: mm ", distance)
        print("#####")
        
        print(type(distance))
        distance = str(distance)
        print(type(distance))
        return distance
        
    def SenserdataSend(self, fn, distance, green_led, mode, time): # 作成した経路表に基づく距離データの送信
        _peripheral.periph(fn, distance, green_led, mode, time)

def MGDist(fn, Pmode_change, Cmode_change):
    #global mode_change
    mg = ManegementDist()
    distance = mg.getdistance()
    #distance = "50"
    
    mg.SenserdataSend(fn, distance, green_led, Pmode_change, time=15) #P:3
    
if __name__ == "__main__":
    fn = 'info/SN02.json'
    Pmode_change = 3
    Cmode_change = 3
    MGDist(fn, Pmode_change, Cmode_change)
