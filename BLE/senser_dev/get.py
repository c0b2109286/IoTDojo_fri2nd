import time
from machine import I2C,Pin
from vl53l1x import VL53L1X

""" パラメータ """
I2C_SCL_PIN = 22  #自分で指定
I2C_SDA_PIN = 21  #自分で指定
""" パラメータ(終わり) """
i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))

def distance():
    #取得データ
    distance = VL53L1X(i2c) #20mm~400mm
    count = 0

    #while True:
    if count is 0:
        distance = distance.read()
        #print(type(distance))
        time.sleep_ms(1000)
        #distance.read()
        count += 1
    print("range: mm ", distance)
    return distance

if __name__ == "__main__":
    distance()
