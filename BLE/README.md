# BLE
## Overview
`relay01_dev`，`relay02_dev`，`senser_dev`それぞれをESP32で実行することでBLEマルチホップ通信が可能．また，`demo_server`を自身のコードエディタの環境内で実行することでFlaskサーバを立ててデータを受け取り，そのデータをhtmlに埋め込むことで確認することが出来る．
### [relay01_dev](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay01_dev)
中継器として`senser_dev`から受信したデータを`relay01_dev`へ送信したり，経路データから経路表を作成する．
### [relay02_dev](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay02_dev)
中継器として`relay01_dev`から受信したデータをサーバへ送信する．
### [senser_dev](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev)
送信機としてセンサーでデータを取得したり，取得データを`relay01_dev`へ送信したりする．  
また，経路データから経路表の作成を行う．
### [demo_server](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/demo_server)
Flaskサーバを立ち上げ，`relay02_dev`からデータを受け取る．
また，データをテンプレートのhtml`view.html`に埋め込むことでwebページとして閲覧が可能となる．
## MindMap
<img src="png/mindmap.png" width="700">

## BLE通信 役割
各機器の動作は主に機器間におけるBLE通信によるデータの送受信であり，特定の機器ではデータの計測やサーバへのデータの送受信が行われる．  
- Peripheral(ペリフェラル)  
親機(送信側)としての動作，`～peripheral`と名の付くファイルが該当．  
- Central(セントラル)  
子機(受信側)としての動作，`～central`と名の付くファイルが該当．  
- Get  
モジュールを用いて距離データの取得を行う，`get`と名の付くファイルが該当．  
- Makeroute  
経路表の作成を行う，`makeroute`と名の付くpythonが該当．
- Manegement  
1デバイスで順々に行われる動作を統括する． `manegement`と名の付くファイルが該当． 

## 詳細
各役割において共通する動作が多い．それぞれを抜粋して説明を行う．
### 1, Peripheral  
#### Overview

1, サーバへの通信時に経由する機器の名前を取得し，中継した機器の数と共にデータを送信する．  
2, センサモジュールで取得した距離データを経路表に則り，サーバまで送信する．  

該当file：
[routedata_peripherals1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/routedata_peripherals1.py) / 
[senddistance_peripherals1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/senddistance_peripherals1.py) / [routedata_peripheral01.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay01_dev/routedata_peripheral01.py) / 
[senddistance_peripheral01.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay01_dev/senddistance_peripheral01.py)  
主な import file : 
[BLE_advertising](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/BLE_advertising.py) /
[manegement_s1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/manegement_s1.py) 

#### Code
- def _payload_1() / def _payload_2()  
機器がアドバタイズを行う際のペイロードを作成し，それを設定する．  
_payload_1 : パケットのペイロード(データ部分)を格納する変数．
- ペイロードにはデバイス名とサービスUUIDを含む．
> UUID : BLEデバイスやサービスを識別するための一意の識別子．
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


### 2, Central
#### Overview
サーバから送られてくる通信経路表を作成する為のデータを取得する.  
該当file : 
[routeget_centrals1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/routeget_centrals1.py) / 
[routedata_central01.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay01_dev/routedata_central01.py) / 
[senddistance_central01.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay01_dev/senddistance_central01.py) / 
[routedata_central02.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay02_dev/routedata_central02.py) / 
[senddistance_central02.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay02_dev/senddistance_central02.py)  
主な import file : 
[BLE_advertising](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/BLE_advertising.py) /
[manegement_s1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/manegement_s1.py)

- handle  
  BLE機器との通信でリソースや属性(キャラクタリスティック)を識別，管理する為の識別子  
  > ・_comm_handle : 接続ハンドル(接続中のデバイスを特定するため)  
  > ・_start_handle / _end_handle : サービスに関連付けされた属性の範囲を識別．  
  > ・_value_handle : 特定の属性の値にアクセスするための識別子．  
  (データの読み取り/通知の受信)

#### Code
BLEデバイスからのデータを読み取るために，print関数をコールバックとして使用する．
適切に処理する為にカスタムコールバック関数が用いられる．
```python senser_dev/routeget_centrals1.py
def read(self, callback):
    if not self.is_connected():
        return
    self._read_callback = callback
    self._ble.gattc_read(self._conn_handle, self._value_handle) # リモート読み込み
    # ...
def Centr():
    # ...
    count = 0
    while count < 3:
        # BLEデバイスからのデータを読み取り、print関数をコールバックとして指定
        central.read(callback=print)  
        print("#####")
        utime.sleep_ms(2000)
        count += 1
        print(count)
```
> binascii.hexlify は、バイナリデータを16進数文字列に変換する関数です．これにより、バイナリデータを人間が読み取りやすい形式に変換できます．  
> binascii.unhexlify はその逆の処理を行います。16進数文字列をバイナリデータに戻します．  16進数文字列からバイナリデータへの変換を行うために使用されます．  

### 3, Get
#### Overview
送信機の役割を持つデバイス用のコード．センサーでのデータ収集と送信などを行う．  
距離センサによって距離(mm)を計測し，結果をreturnする．  
該当 file : 
[get_s1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/get_s1.py) / 
主な import file: [vl53l1x](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/vl53l1x.py)
#### Code  
`get_s1.py`のコメントアウトに記載．


### 4, Makeroute
#### Overview
受け取った経路データを用いて経路表を作成する．  
該当 file : 
[makeroute_s1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/makeroute_s1.py) / 
[makeroute_01.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/relay01_dev/makeroute_01.py)
主な import file : 
[makeroute_data.txt](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/data/makeroutedata_s1.txt) /
[packet_table.json](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/data/packet_table.json)
#### Code
`makeroute_s1.py`のコメントアウトに記載．

### 5, Manegement
#### Overview
センサデバイスの動作を統括する．  
該当 file : 
[manegment_s1.py](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/manegment_s1.py)

import file : 
[routedata_peripherals1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/routedata_peripherals1.py) /
[routeget_centrals1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/routeget_central_s1.py) / 
[senddistance_peripherals1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/senddistance_peripherals1.py) / 
[makeroute_s1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/makeroute_s1.py) / 
[get_s1](https://github.com/Fel615/IoTDojo_fri2nd/blob/main/BLE/senser_dev/get_s1.py)

#### Code
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
