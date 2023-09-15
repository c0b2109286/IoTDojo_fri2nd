import ujson
import bluetooth
import random
import struct
import time
import binascii
from BLE_advertising import advertising_payload
import get
import info
import json

from micropython import const

# BLEイベントの定数
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

# BLEフラグの定数
_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# デバイス情報サービス
_Dev_Info_UUID = bluetooth.UUID(0x180A)
# デバイスの名前
_Dev_CHAR = (bluetooth.UUID(0x2A00), _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,)  # 読み取り、通知、応答要求付き通知
_Dev_SERVICE = (_Dev_Info_UUID, (_Dev_CHAR,),)

# BLE関連のクラス
class BLE:
    ble = None
    name = None
    
    def __init__(self, ble, name):
        self._ble = ble
        self._name = name
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_Dev_SERVICE,))
        self._connections = set()
        self._check = False
        
    def _payload_1(self, name):
        self._name = name
        self._payload_1 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance=0)
        self._advertise_1()
        
    def _payload_2(self, name):
        self._name = name
        self._payload_2 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance=0)
        self._advertise_2()
        
    def _irq(self, event, data):
        # 接続を追跡して通知を送信できるようにします。
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self._check = True
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # 新しい接続を許可するために再度広告を開始します。
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def set_dev_name(self, data, notify=False, indicate=False):
        # データは摂氏温度で、0.01度の分解能を持っています。
        # ローカル値を書き込んで、セントラルが読み取るのに備えます。
        self._ble.gatts_write(self._handle, struct.pack('12si', data)) #読み込み可能な書き込み
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # 接続されたセントラルに通知
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # 接続されたセントラルに指示
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise_1(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_1)

    def _advertise_2(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_2)

    def _stop(self, interval_us=None):
        self._ble.gap_advertise(interval_us)

# メインのペリフェラル関数
def periph(distance, timeout):
    i = 0
    flag = 0
    data = None
    name = None

    jf_open = open('info/SN01.json', 'r')
    jf_load = json.load(jf_open)
    gapname = jf_load["device_number"]
    
    ble = bluetooth.BLE()
    ble.config(gap_name= gapname)
    set_name = ble.config('gap_name')
    b = BLE(ble, name)
    
    set_name = set_name.decode()
    str_flag = str(flag)
    
    print(distance)
    print(type(distance))

    route = ujson.loads(open("data/routeinfo.json").read())
    
    # デバッグ用: ルート情報を表示
    # print(route.values())
    # print(route["relay01"])
    # print(route["relay11"])
    
    jf_open = open('info/SN01.json', 'r')
    jf_load = json.load(jf_open)
    gapname = jf_load["device_number"]
    
    if b._check is False and flag == 0:
        b._payload_1(route["relay01"])
        while b._check is False and timeout > 0:
            data = gapname + '_' + distance
            i = (i + 1) % 10
            b.set_dev_name(data, notify=i == 0, indicate=False)
            payload = binascii.hexlify(b._payload_1)
            pay1 = str(binascii.unhexlify(payload), 'utf-8')
            print(pay1)
            print('.')
            time.sleep_ms(1000)
            timeout -= 1

    if b._check is False:
        print("change")
        flag = 1
        str_flag = str(flag)
        print(type(str_flag))
        print(type(flag))
        print(flag)
        timeout = 10
        
    if b._check is False and flag == 1:
        b._payload_2(route["relay11"])
        while b._check is False and timeout > 0:
            data = gapname + '_' +distance
            i = (i + 1) % 10
            b.set_dev_name(data, notify=i == 0, indicate=False)
            payload = binascii.hexlify(b._payload_2)
            pay2 = str(binascii.unhexlify(payload), 'utf-8')
            print(pay2)
            print('*')
            time.sleep_ms(1000)
            timeout -= 1

    if b._check is False:
        print("conection faild")
    else:
        print("conected")
        print(data)

    b._stop()
    print("終了")

if __name__ == "__main__":
    periph()
