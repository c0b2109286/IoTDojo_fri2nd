# For senser_dev
送信機の役割を持つデバイス用のコード．センサーでのデータ収集と送信などを行う．
## [get_s1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/get_s1.py)
### Overview
距離センサによって距離(mm)を計測し，結果をreturnする．  
import file: [vl53l1x](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/vl53l1x.py)


## [makeroute_s1.py](https://github.com/c0b2107561/dojo_Pvt./blob/main/senser_dev/makeroute_s1.py)
### Overview
受け取った経路データを用いて経路表を作成する．  
import file : 
[makeroute_data.txt](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/data/makeroutedata_s1.txt) /
[packet_table.json](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/data/packet_table.json)


## [manegment_s1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/manegment_s1.py)
### Overview
センサデバイスの動作を統括する．   
import file : 
[routedata_peripherals1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/routedata_peripherals1.py) /
[routeget_centrals1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/routeget_central_s1.py) / 
[senddistance_peripherals1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/senddistance_peripherals1.py) / 
[makeroute_s1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/makeroute_s1.py) / 
[get_s1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/get_s1.py)

### Code
デバイスの基本情報を定義する．  
> デバイス番号...　各デバイスの判別，経路データ．  
> パケット名...　受け取るデータの選別．  
> 用途(センサ or 中継器)...　経路表のkey → 経路選択．  
```python senser_dev/manegment_s1.py
def nameinfo():
    dev_name = 8 # デバイス番号
    return dev_name
def packetinfo():
    dev_packet = "esp32-1A" # パケット名
    return dev_packet
def positioninfo():
    dev_position = "senser01" # 用途
    return dev_position
```

- 関数により呼び出されるモジュール(importファイル)と用途

|関数|ファイル|詳細|
|:---|:---|:---|
|_RoutedataSend|routedata_peripherals1.py|データに自身のデバイス名と追加し，中継器のホップ数をカウントすることで作成されるデータを通信経路データとし，サーバを終点としてデータを送信する．|
|_RoutedataGet|routeget_centrals1.py|サーバで加工(経路の優先順位を追加)された経路表作成用のデータを受け取る．|
|_RoutedataWrite|×|経路表作成の為に取得したデータをテキストファイルに書き込み，保存する．|
|_check|×|確認用|  


## [routdata_peripherals1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/routedata_peripherals1.py)
### Overview
サーバへの通信時に経由する機器の名前を取得し，中継した機器の数と共にデータを送信する．  
import file : 
[BLE_advertising](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/BLE_advertising.py) /
[manegement_s1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/manegement_s1.py) 

- UUID
  BLEデバイスやサービスを識別するための一意の識別子．

### Code
- def _payload_1() / def _payload_2()  
機器がアドバタイズを行う際のペイロードを作成し，それを設定する．  
_payload_1 : パケットのペイロード(データ部分)を格納する変数．  
> ペイロードにはデバイス名とサービスUUIDを含む．
``` python senser_dev/routedata_peripherals1.py
def _payload_1(self, name):
    self._name = name
    self._payload_1 = advertising_payload(
        name=name, services=[_Dev_Info_UUID], appearance=0)
    self._advertise()
```

- def _irq()
機器がセントラルとの接続状態を管理する為のイベント処理．  
> _IRQ_CENTRAL_CONNECT : 接続イベント  
> _IRQ_CENTRAL_DISCONNECT : 切断イベント  
> _IRQ_GATTS_INDICATE_DONE : 通知完了イベント
``` python senser_dev/routedata_peripherals1.py
if event == _IRQ_CENTRAL_CONNECT:　
    conn_handle, _, _ = data
    self._connections.add(conn_handle)
    # 接続後，アドバタイズを終了する．
    self._check = True
elif event == _IRQ_CENTRAL_DISCONNECT:
    conn_handle, _, _ = data
    self._connections.remove(conn_handle)
    # 新しい接続を許可するために再びアドバタイズを開始する．
    self._check = False
    self._advertise()
elif event == _IRQ_GATTS_INDICATE_DONE:
    conn_handle, value_handle, status = data
```
