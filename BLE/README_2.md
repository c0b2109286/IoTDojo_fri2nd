# ESP32 BLE通信
## Peripheral
### peripheral.py [peripheralの役割をするコード]
### 【関数】

- def __init__(self, ble, name):

  初期化
- def _irq(self, event, data):

  イベント処理
- def set_dev_name(self, dev_name, notify=False, indicate=False):

  ローカル値の編集や読み取り、接続機器への要求送信
- def _advertise(self, interval_us=500000):

  アドバタイジングの実行
- def BLE_adv():

  BLEの設定と実行



### 【処理】

- _Dev_Info_UUID = bluetooth.UUID(0x180A)

  service UUIDの設定
- _Dev_CHAR = (bluetooth.UUID(0x2A00), bluetooth.FLAG_READ|bluetooth.FLAG_WRITE,)

  Characteristics(UUID,FLAG)の設定
- ((self._handle,),) = self._ble.gatts_register_services((_Dev_SERVICE,))

  指定したサービスでサーバを構成し、既存のサービスを置換
- self._payload = advertising_payload(
        name=name, services=[_Dev_Info_UUID], appearance=0)

  from import したdef関数を用いてペイロードを作成
- self._ble.gatts_write(self._handle, struct.pack('12si',dev_name)) 

  ハンドルのローカル値を書き込む
- struct.pack(fmt,value)

  フォーマット文字列fmtにしたがって値valueをパックする
- self._ble.gatts_notify(conn_handle, self._handle)

  接続されたセントラルに読み取りを発行するよう通知する         
- name = ble.config(gap_name='senser01')

  GAPデバイス名の設定
- dev_name = binascii.unhexlify(name_enc)

  16進データをバイナり表現に変換する

### 【イベントコード/UUID/Flag/fmt】
- _IRQ_CENTRAL_CONNECT = const(1)
  
  セントラルがこの周辺機器に接続
- _IRQ_CENTRAL_DISCONNECT = const(2)

  セントラルがこの周辺機器から切断
- 0x180A :Service/Device Infomation service
- 0x2A00 :Characteristics/Device Name
- FLAG_READ : ローカル値の読み取り
- FLAG_WRITE : ローカル値の書き込み
- 12si : 12→12文字, s→文字列をバイト列に変換したもの, i→整数(iは要らない？)

## Central
### central.py [centralの役割をするコード]
### 【クラス，関数】
```python:central.py
class BLEDevCentral 
  def form_mac_address(addr: bytes) -> str:
    bytes型のマックアドレスをstr型へ変換する為の関数
  def bt_irq(event, data):
    イベントを喚起してそれぞれ処理を定める為の関数．
  def is_connectes(self):
    機器が別機器と接続している状況の場合に実行される関数．
  def scan(sel, callback=None):
    機器がスキャンを行う為の関数
  def connect(self, addr_type=None, addr=None, callback=None):
    機器が接続を行う為の関数
  def disconnect(self):
    機器が接続を切る為の関数
  def read(self, callback):
    アドバタイズパケットの読み込みを行う為の関数
  def on_notify(self, callback):
    通知を行う為の関数
  def _updata_value(self, value):
    データをアップデートする為の関数
  def value(self):
    データを返す為の関数
def Centr()
    順にクラス内の関数を呼び出し処理を実行する為の関数
```
### 【処理】
- ble.active(True)

  BLEを起動する

- ble.irq(bt_irq)

  イベント処理

- ble.gap_scan(interval_ms, interval_us, window_us,active = False,)

  ・スキャンを行う

  ・スキャナは全体の duration_ms ミリ秒の間の interval_us マイクロ秒毎に window_us マイクロ秒間実行する
  
  ・スキャンの応答を結果として受け取りたい場合は、 active を True にする

### 【イベントコード/UUID】
- _IRQ_SCAN_RESULT = const(5)

  シングルスキャン結果
- _IRQ_SCAN_DONE = const(6)

  スキャン期間が終了したか、手動で停止した
