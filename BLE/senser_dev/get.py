import time
from machine import I2C,Pin
from vl53l1x import VL53L1X

# I2C通信のSCLピン（クロック）とSDAピン（データ）を指定して,I2Cインターフェースを初期化する．
#I2C_SCL_PIN = 22  
#I2C_SDA_PIN = 21
#i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))


def distance(i2c):
    #i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
    
  # 距離センサーであるVL53L1Xのインスタンスを作成して初期化する．
  # センサーは20mmから400mmまでの範囲で距離を測定可能，
  distance = VL53L1X(i2c)
  count = 0 #count 変数を定義して初期値を0に設定する．

  # count が0の場合、距離センサーから距離データを読み取り，その後、1秒待機する．
  if count is 0: 
    distance = distance.read()
    time.sleep_ms(1000)
    count += 1
  # 距離データを出力し、その値を返す．
  print("range: mm ", distance)
  return distance

if __name__ == "__main__":
    I2C_SCL_PIN = 22  
    I2C_SDA_PIN = 21
    i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
    distance(i2c)
