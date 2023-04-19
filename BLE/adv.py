import ubluetooth
import random
import struct
import time
import binascii
from micropython import const
from BLE_advertising import advertising_payload

_IRQ_CENTRAL_CONNECT                 = const(1)
_IRQ_CENTRAL_DISCONNECT              = const(2)

# デバイス情報サービス
_Dev_Info_UUID = ubluetooth.UUID(0x180A)
# デバイス名
_Dev_CHAR = (ubluetooth.UUID(0x2A7D), ubluetooth.FLAG_READ|ubluetooth.FLAG_WRITE,)
_Dev_SERVICE = (_Dev_Info_UUID, (_Dev_CHAR,),)

class BLE:

    ble = None
    name = None

    def __init__(self, ble,name):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_Dev_Info_UUID,))
        self._connections = set()
        self._payload = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance=0)
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle) #要素追加
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle) #要素削除
            # Start advertising again to allow a new connection.
            self._advertise() #advertiseに戻る

    def set_dev_name(self, dev_name, notify=False, indicate=False):
        # Data is sint16 in degrees Celsius with a resolution of 0.01 degCelsius.
        # Write the local value, ready for a central to read.
        self._ble.gatts_write(self._handle, dev_name) #ハンドルのローカル値を書き込む
        if notify: #flag書き換え必須
            for conn_handle in self._connections:
                # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._handle) #通知要求を送信

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)


def BLE_adv():
    ble = ubluetooth.BLE
    name = ble.config(gap_name='senser01')
    name_enc = name.encode('utf-8') #文字コード(16進数)へ変換
    dev_name = binascii.unhexlify(name_enc) #byte型(バイナリデータ)へ変換
    b = BLE(ble, dev_name)

    i = 0
    count = 0

    #二回データを出す 
    while count < 2:
        i = (i + 1) % 10
        b.set_dev_name(dev_name, notify=i == 0, indicate=False)
        print(dev_name)
        time.sleep_ms(1000)
        count += 1

if __name__ == "__main__"():
    BLE_adv()