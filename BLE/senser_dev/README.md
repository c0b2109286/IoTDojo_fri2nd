# For senser_dev
送信機の役割を持つデバイス用のコード．センサーでのデータ収集と送信などを行う．
## [get_s1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/get_s1.py)
### Overview
距離センサによって距離(mm)を計測し，結果をreturnする．  
import file: [vl53l1x](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/vl53l1x.py)

### Code
```python senser_dev/get_s1.py
I2C_SCL_PIN = 22  
I2C_SDA_PIN = 21  
```
I2C通信のSCLピン（クロック）とSDAピン（データ）を指定して,I2Cインターフェースを初期化する．

```python senser_dev/get_s1.py
def distance():
  # 距離センサーであるVL53L1Xのインスタンスを作成して初期化する．
  # センサーは20mmから400mmまでの範囲で距離を測定可能，
  distance = VL53L1X(i2c)
  # count = 0 #count 変数を定義して初期値を0に設定する．

  # count が0の場合、距離センサーから距離データを読み取り，その後、1秒待機する．
  if count is 0: 
    distance = distance.read()
    time.sleep_ms(1000)
    count += 1
  # 距離データを出力し、その値を返す．
  print("range: mm ", distance)
  return distance
```
VL53L1Xセンサーを初期化し、一度だけ距離を読み取って表示する．

## [makeroute_s1.py](https://github.com/c0b2107561/dojo_Pvt./blob/main/senser_dev/makeroute_s1.py)
### Overview
受け取った経路データを用いて経路表を作成する．  
import file : 
[makeroute_data.txt](https://github.com/c0b2107561/dojo_Pvt./blob/main/senser_dev/data/makeroutedata_s1.txt) /
[packet_table.json](https://github.com/c0b2107561/dojo_Pvt./blob/main/senser_dev/data/packet_table.json)

### Code
```python senser_dev/makeroute_s1.py
import ujson
from collections import OrderedDict

class RouteMake:
  def _readtxt(self):
        split = []
        with open("data/makeroute_data.txt",'r',encoding="utf-8")as f:
            data = f.readlines()
            for i in range(len(data)):
                data[i] = data[i].split('_')
                for j in range(len(data[i])):
                    if '\r' in data[i][j]:
                        data[i][j] = data[i][j].replace('\r', '')
                    if '\n' in data[i][j]:
                        data[i][j] = data[i][j].replace('\n', '')
                split.append(data[i])
            print(split)
            f.close()
            return split
```
テキストファイルからデータを読み込んでlistにする関数

```python senser_dev/makeroute_s1.py
  def _makeval(self,split):
        with open("data/packet_table.json", 'r', encoding="utf-8") as f:
            table= ujson.load(f)
            print("@@@@@")
            print(table)
            print(split)
            print(type(table))
            # for key in table.keys():
            #     print(key)
            print('---------')
            lis = []

            for i in range(len(split)):
                ls = []
                for list in split[i][:-2]:
                    print(list)
                    # print(type(list))
                    ls.append(table[list])
                lis.append(ls)
            print(lis)
            return lis
```
JSONファイルから値を取得して二重リストを作成する関数.

```python senser_dev/makeroute_s1.py
  def _makekey(self, lis):
      print("$$$$$$$$$")
      _lis = []
      for i in range(len(lis)):
          _ls = []
          for j in range(len(lis[i])):
              if j == 0:
                  _ls.append('senser'+ str(i) + str(j))
              else:
                  _ls.append('relay'+ str(i) + str(j))
          _lis.append(_ls)
      print(_lis)
      return _lis
```
_makeval関数にて作成したリストを参考に辞書のキーとなる二重リストを作成する関数．

```python senser_dev/makeroute_s1.py
  def _dict(self, split, val, key):
          dic = OrderedDict() #順序付き辞書の作成
          for i in range(len(key)):
              if i == 0:
                  dic.update(OrderedDict(zip(key[i], val[i])))
                  hopnum = split[i][-2]
                  dic['hop' + str(i)] = hopnum
                  rank = split[i][-1]
                  dic['rank' + str(i)] = rank
              else:
                  dic.update(OrderedDict(zip(key[i], val[i])))
                  hopnum = split[i][-2]
                  dic['hop' + str(i)] = hopnum
                  rank = split[i][-1]
                  dic['rank' + str(i)] = rank
          return dic
```
_makeval関数と_makekey関数によって作成したリストを用いて辞書を生成する関数．

```python senser_dev/makeroute_s1.py
  def _json(self, dic):
          with open('routeinfo.json', 'w', encoding="utf-8") as f:
              num = len(dic)
              ujson.dump(dic, f)
```
_dict関数によって作成したリストをJSONファイルに書き込む関数．

``` python senser_dev/makeroute_s1.py
def _routemake():
    rm = RouteMake()
    split = rm._readtxt()
    val = rm._makeval(split)
    key = rm._makekey(val)
    dic = rm._dict(split, val, key)
    rm._json(dic)
```
main関数

``` python senser_dev/makeroute_s1.py
if __name__ == "__main__":
    _routemake()
```
main関数を呼び出し，経路表を作成する．
