# This example demonstrates a simple temperature sensor peripheral.
#
# The sensor's local value updates every second, and it will notify
# any connected central every 10 seconds.

import bluetooth
import random
import struct
import utime
import binascii
from BLE_advertising import advertising_payload
import info
import ujson


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

connect_count = 0

class BLE:

    ble = None
    name = None

    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_Dev_SERVICE,))
        self._connections = set()
        self._check = False
        #self._connect_count = 0

    def _payload_1(self, name):
        self._name = name
        self._payload_1 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance= 0)
        self._advertise1()
        
    def _payload_2(self, name):
        self._name = name
        self._payload_2 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance= 0)
        self._advertise2()
        
    def _payload_3(self, name):
        self._name = name
        self._payload_3 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance= 0)
        self._stop1()
        
    def _payload_4(self, name):
        self._name = name
        self._payload_4 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance= 0)
        self._stop2()


    def _irq(self, event, data):
        # Track connections so we can send notifications.
        global connect_count
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self._check = True
            utime.sleep_ms(100)
            #self._check = False
            connect_count += 1
            print(connect_count)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._check = False
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def set_dev_name(self, name, notify=False, indicate=False):
        # Data is sint16 in degrees Celsius with a resolution of 0.01 degrees Celsius.
        # Write the local value, ready for a central to read.
        fm = '{}si'.format(len(name))
        self._ble.gatts_write(self._handle, struct.pack(fm,name)) #読み込み可能な書き込み
        #self._ble.gatts_write(self._handle, name)
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # Notify connected centrals.
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # Indicate connected centrals.
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise1(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_1)
        
    def _advertise2(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_2)

    def _stop1(self, interval_us = None):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_3)
    
    def _stop2(self, interval_us = None):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_4)


def periph(fn, data, _led, mode, timeout):
    global connect_count
    
    ble = bluetooth.BLE()
    jf_load = ujson.loads(open(fn).read())
    gapname = jf_load["device_number"]
    
    ble.config(gap_name= str(gapname))
    set_name = ble.config('gap_name')
    print(set_name)    
    print(type(set_name))
    
    
    name = set_name
    name = set_name.decode('utf-8')
    print(type(name))
    
    b = BLE(ble)
 
    i = 0
    connect_count = 0
    print(mode)
    print(timeout)

    if mode is 0:
        b._payload_1(str(jf_load["packet_name_routeT2"]))
        while timeout is not 0 and b._check is False:
        #while timeout is not 0:
            if b._check is False:
                i = (i + 1) % 10
                b.set_dev_name(data, notify=i == 0, indicate=False)
                print(".")
                utime.sleep(0.5)
                _led.off()
                utime.sleep(0.5)
                timeout -=1
        if timeout is 0 or connect_count is 1:
            utime.sleep(3)
            b._payload_3("stop")
            connect_count = 0
            print("終了")
            _led.off()
                
    if mode is 1:
        print(data)
        b._payload_2(str(jf_load["packet_name_routeT4"]))
        while timeout is not 0 and b._check is False:
        #while timeout is not 0:
            if b._check is False:
                i = (i + 1) % 10
                b.set_dev_name(data, notify=i == 0, indicate=False)
                print(".")
                utime.sleep(0.5)
                _led.off()
                utime.sleep(0.5)
                timeout -=1
        if timeout is 0 or connect_count is 1:
            utime.sleep(3)
            b._payload_4("stop")
            connect_count = 0
            print("終了")
            _led.off()
            
    if mode is 2:
        b._payload_1(str(jf_load["packet_name_routeT4"]))
        while timeout is not 0 and b._check is False:
        #while timeout is not 0:
            if b._check is False:
                i = (i + 1) % 10
                b.set_dev_name(data, notify=i == 0, indicate=False)
                print(".")
                utime.sleep(0.5)
                _led.off()
                utime.sleep(0.5)
                timeout -=1
        if timeout is 0 or connect_count is 1:
            utime.sleep(3)
            b._payload_3("stop")
            print("終了")
            _led.off()
                
    if mode is 3:
        b._payload_2(str(jf_load["packet_name_routeT4"]))
        while timeout is not 0 and b._check is False:
        #while timeout is not 0:
            if b._check is False:
                i = (i + 1) % 10
                b.set_dev_name(data, notify=i == 0, indicate=False)
                print(".")
                utime.sleep(0.5)
                _led.off()
                utime.sleep(0.5)
                timeout -=1
        if timeout is 0 or connect_count is 1:
            utime.sleep(3)
            b._payload_4("stop")
            print("終了")
            _led.off()
            
    print("終了")
    _led.off()

if __name__ == "__main__":
    timeout = 10
    routedata = "5"
    fn = 'info/DN01.json'
    red_pin = 13
    _led = machine.Pin(red_pin, machine.Pin.OUT)
    mode = 0
    periph(fn, routedata, _led, mode, timeout)
