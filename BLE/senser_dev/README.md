# For senser_dev
送信機の役割を持つデバイス用のコード．センサーでのデータ収集と送信などを行う．
## [get_s1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/get_s1.py)
### Overview
距離センサによって距離(mm)を計測し，結果をreturnする．  
import : [vl53l1x](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/vl53l1x.py)

### Code
```python senser_dev/get_s1.py
I2C_SCL_PIN = 22  
I2C_SDA_PIN = 21  
```
I2C通信のSCLピン（クロック）とSDAピン（データ）を指定して,I2Cインターフェースを初期化する，

```python senser_dev/get_s1.py
def distance():
  #距離センサーであるVL53L1Xのインスタンスを作成して初期化する．
  センサーは20mmから400mmまでの範囲で距離を測定可能，
  distance = VL53L1X(i2c)
  #count = 0 #count 変数を定義して初期値を0に設定する．

  #count が0の場合、距離センサーから距離データを読み取り，その後、1秒待機する．
  if count is 0: 
    distance = distance.read()
    time.sleep_ms(1000)
    count += 1
  # 距離データを出力し、その値を返す．
  print("range: mm ", distance)
  return distance
```
VL53L1Xセンサーを初期化し、一度だけ距離を読み取って表示する．
