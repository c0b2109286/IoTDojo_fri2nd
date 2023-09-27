#com8 peripheral code

import ujson
import bluetooth
import random
import struct
import time
import binascii
from BLE_advertising import advertising_payload

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# デバイス情報サービス
_Dev_Info_UUID = bluetooth.UUID(0x180A)
# デバイスの名前
_Dev_CHAR = (bluetooth.UUID(0x2A00),
    _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,) #読、通知、応答要求付き通知
_Dev_SERVICE = (_Dev_Info_UUID,(_Dev_CHAR,),)

class BLE:

    ble = None
    name = None
    
    def __init__(self, ble,name):
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
            name=name, services=[_Dev_Info_UUID], appearance= 0)
        self._advertise_1()
        
    def _payload_2(self, name):
        self._name = name
        self._payload_2 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance= 0)
        self._advertise_2()
        
    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self._check = True
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def set_dev_name(self, data, notify=False, indicate=False):
        # Data is sint16 in degrees Celsius with a resolution of 0.01 degrees Celsius.
        # Write the local value, ready for a central to read.
        self._ble.gatts_write(self._handle, struct.pack('12si',data)) #読み込み可能な書き込み
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # Notify connected centrals.
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # Indicate connected centrals.
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise_1(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_1)

    def _advertise_2(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_2)

    #def _stop(self, interval_us):
    #    self._ble.gap_advertise(interval_us, adv_data=self._payload)


def periph(distance,timeout=10):
    
    i = 0
    flag = 0
    data = None
    name = None
    
    ble = bluetooth.BLE()
    ble.config(gap_name='8')
    set_name = ble.config('gap_name')
    b = BLE(ble,name)
    
    print(type(set_name))
    set_name = set_name.decode()
    print(type(set_name))
    str_flag = str(flag)
    print(type(str_flag))
    print(type(flag))

    route = ujson.loads(open("data/routeinfo.json").read())
    #info = ujson.loads(open("setinfo.json").read())
    #print(route.values())
    #print(info.values())
    #print(route["relay01"])
    #print(binascii.hexlify(route["relay01"]))
    #print(route["relay11"])
    #print(binascii.hexlify(route["relay11"]))
    
    
    if b._check is False and flag == 0:
        #b._payload_1("esp32-3A")
        b._payload_1(route["relay01"])
        while b._check is False and timeout > 0:
            #Write every second, notify every 10 seconds.
            #data = set_name + ',' + str_flag
            #b._name = file["next_1"]
            data = distance
            i = (i + 1) % 10
            b.set_dev_name(data, notify=i == 0, indicate=False)
            payload = binascii.hexlify(b._payload_1)
            pay1 = str(binascii.unhexlify(payload), 'utf-8')
            #pay1 = int(binascii.unhexlify(payload), 16)
            print(pay1)
            ##Random walk the temperature.
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
        #b._payload_2("esp32-3A")
        b._payload_2(route["relay11"])
        while b._check is False and timeout > 0:
            #Write every second, notify every 10 seconds.
            data = set_name + ',' + str_flag
            #b._name = file["next_2"]
            data = distance
            i = (i + 1) % 10
            b.set_dev_name(data, notify=i == 0, indicate=False)
            payload = binascii.hexlify(b._payload_2)
            pay2 = str(binascii.unhexlify(payload), 'utf-8')
            #pay2 = int(binascii.unhexlify(payload), 16)
            print(pay2)
            ##Random walk the temperature.
            print('*')
            time.sleep_ms(1000)
            timeout -= 1

    if b._check is False:
        print("conection faild")
        
    else:
        print("conected")
        print(data)

    print("終了")

if __name__ == "__main__":
    periph()

