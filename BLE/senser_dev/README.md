# For senser_dev
送信機の役割を持つデバイス用のコード．センサーでのデータ収集と送信などを行う．
## [get_s1.py](https://github.com/c0b2107561/dojo_Pvt./blob/main/senser_dev/get_s1.pyS)
### Overview
距離センサによって距離(mm)を計測し，結果をreturnする．  
import : [vl53l1x](https://github.com/c0b2107561/dojo_Pvt./blob/main/senser_dev/vl53l1x.py)

### Code
```python senser_dev/get_s1.py
I2C_SCL_PIN = 22  
I2C_SDA_PIN = 21  
```
