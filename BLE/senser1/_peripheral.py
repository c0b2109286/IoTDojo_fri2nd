import bluetooth
import random
import struct
import utime
import binascii
from BLE_advertising import advertising_payload
import info
import ujson
from machine import I2C,Pin
from vl53l1x import VL53L1X
import machine

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

#red_pin = 13
#red_led = machine.Pin(red_pin, machine.Pin.OUT)
#green_pin = 14
#green_led = machine.Pin(green_pin, machine.Pin.OUT)
#blue_pin = 15
#blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

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
        self._connect_count = 0
        
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
        
    def _payload_3(self, name="stop"):
        self._name = name
        self._payload_3 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance=0)
        self._stop1()
        
    def _payload_4(self, name="stop"):
        self._name = name
        self._payload_4 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance=0)
        self._stop2()
        
    def _irq(self, event, data):
        # 接続を追跡して通知を送信できるようにします。
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self._check = True
            self._connect_count += 1
            print(f"connection : {self._connect_count}")
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # 新しい接続を許可するために再度広告を開始します。
            #self._advertise()
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

    def _advertise_1(self, interval_us=100000): #0.1秒間隔
        self._ble.gap_advertise(interval_us, adv_data=self._payload_1)

    def _advertise_2(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_2)

    def _stop1(self, interval_us=None):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_3)
        
    def _stop2(self, interval_us=None):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_4)
        
    def _key(self, nd):
        with open('data/packet_table.json', 'r') as file:
            data = ujson.load(file)
            
        target_val = nd
        target_key = 0
        
        for key, value in data.items():
            if value == target_val:
                target_key = key
        return target_key

# メインのペリフェラル関数
def periph(fn, distance, _led, mode, timeout):
    i = 0
    flag = 0
    #data = None
    name = None
    break_dev = 0
    next_dev = 0
    breaking = 0
    
    jf_load = ujson.loads(open(fn).read())
    gapname = str(jf_load["device_number"])
    
    ble = bluetooth.BLE()
    ble.config(gap_name= str(gapname))
    set_name = ble.config('gap_name')
    b = BLE(ble, name)
    
    # デバッグ用: ルート情報を表示
    # print(route.values())
    # print(route["relay01"])
    # print(route["relay11"])
    
    if mode == 0: #modeが0
        data = set_name
        print(data)
        print(type(data))
        b._payload_1(str(jf_load["packet_routeTS"]))
        print(timeout)
        print(b._connect_count)
        while timeout > 1 or b._connect_count is 0:
            if b._check is False:
                i = (i + 1) % 10
                _led.on()
                b.set_dev_name(data, notify=i == 0, indicate=False)
                print(".")
                utime.sleep(0.5)
                _led.off()
                utime.sleep(0.5)
                timeout -=1

            if timeout is 0 or b._connect_count is 1:
                utime.sleep(1)
                b._payload_3()
                print("終了")
                #mode += 1
                _led.off()
                break
            #b._payload_3(jf_load["packet_routeTS"])
            #b.set_dev_name(data, notify=i == 0, indicate=False)
        return mode
    
    if mode == 1: #modeが1
        data = "route_make_start"
        
        jf_load = ujson.loads(open('data/SenserRouteinfo.json').read())
        packet_name = str(jf_load["senser00"])
        
        b._payload_1(packet_name)
        print(timeout)
        print(b._connect_count)
        while timeout > 1 or b._connect_count is 0:
            if b._check is False:
                i = (i + 1) % 10
                _led.on()
                b.set_dev_name(data, notify=i == 0, indicate=False)
                print(".")
                utime.sleep(0.5)
                _led.off()
                utime.sleep(0.5)
                timeout -=1

            if timeout is 0 or b._connect_count is 1:
                utime.sleep(1)
                b._payload_3()
                print("終了")
                _led.off()
                #mode += 1
                break
            #b._payload_3(jf_load["packet_routeTS"])
            #b.set_dev_name(data, notify=i == 0, indicate=False)
        return mode
    
    if mode < 2: #modeが2
        data = set_name
        b._payload_1(jf_load["packet_routeTS"])
        print(timeout)
        print(b._connect_count)
        while timeout > 1 or b._connect_count is 0:
            if b._check is False:
                i = (i + 1) % 10
                _led.on()
                b.set_dev_name(data, notify=i == 0, indicate=False)
                print(".")
                utime.sleep(0.5)
                _led.off()
                utime.sleep(0.5)
                timeout -=1

            if timeout is 0 or b._connect_count is 1:
                utime.sleep(1)
                b._payload_3(jf_load["packet_routeTS"])
                print("終了")
                #mode += 1
                _led.off()
                break
            #b._payload_3(jf_load["packet_routeTS"])
            #b.set_dev_name(data, notify=i == 0, indicate=False)
        return mode
    
    if mode > 2: #modeが3以上
        set_name = set_name.decode()
        str_flag = str(flag)
        
        print(distance)
        print(type(distance))

        route = ujson.loads(open("data/Routeinfo.json").read())
        
        if b._check is False and flag == 0:
            next_dev = route["relay01"]
            b._payload_1(next_dev)
            while b._check is False and timeout > 0:
                data = gapname + '_' + distance + '_' + str(break_dev)
                print(data)
                i = (i + 1) % 10
                _led.on()
                b.set_dev_name(data, notify=i == 0, indicate=False)
                payload = binascii.hexlify(b._payload_1)
                pay1 = str(binascii.unhexlify(payload), 'utf-8')
                print(pay1)
                print('.')
                utime.sleep(0.5)
                _led.off()
                timeout -= 1
                utime.sleep(0.5)
                if timeout is 0 or b._connect_count is 1:
                    utime.sleep(3)
                    b._payload_3()
                    print("終了")
                    #mode += 1
                    _led.off()
                    break


        if b._check is False:
            print("change")
            breaking = next_dev
            flag = 1
            str_flag = str(flag)
            print(type(str_flag))
            print(type(flag))
            print(flag)
            timeout = 10
            
        if b._check is False and flag == 1:
            next_dev = route["relay11"]
            b._payload_2(next_dev)
            break_dev = b._key(breaking)
            while b._check is False and timeout > 0:
                data = gapname + '_' + distance + '_' + str(break_dev)
                print(data)
                i = (i + 1) % 10
                _led.on()
                b.set_dev_name(data, notify=i == 0, indicate=False)
                payload = binascii.hexlify(b._payload_2)
                pay2 = str(binascii.unhexlify(payload), 'utf-8')
                print(pay2)
                print('*')
                utime.sleep(0.5)
                _led.off()
                utime.sleep(0.5)
                timeout -= 1
                if timeout is 0 or b._connect_count is 1:
                    utime.sleep(3)
                    b._payload_4()
                    print("終了")
                    #mode += 1
                    _led.off()
                    break


        if b._check is False:
            print("conection faild")
        else:
            print("conected")
            _led.off()
            print(data)

        print("終了")
        _led.off()
        return mode

if __name__ == "__main__":
    dist = "11"
    timer = 10
    blue_pin = 14
    _led = machine.Pin(blue_pin, machine.Pin.OUT)
    fn = 'info/SN01.json'
    mode = 0
    periph(fn, dist, _led, mode,  timer)
