import bluetooth
import random
import struct
import utime
import binascii
from BLE_advertising import advertising_payload
# import manegement
import info 
import ujson
import machine
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# デバイス情報サービス
_Dev_Info_UUID = bluetooth.UUID(0x180A)
# デバイスの名前
_Dev_CHAR = (bluetooth.UUID(0x2A00),
    _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,) # 読み取り，通知，応答要求付き通知
_Dev_SERVICE = (_Dev_Info_UUID,(_Dev_CHAR,),)

#blue_pin = 15
#blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

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
        self._connect_count = 0

    def _payload_1(self, name):
        self._name = name
        self._payload_1 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance=0)
        self._advertise()
        
    def _payload_2(self, name):
        self._name = name
        self._payload_2 = advertising_payload(
            name=name, services=[_Dev_Info_UUID], appearance=0)
        self._advertise()
        
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
        # 接続を追跡して通知を送信できるようにする．
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self._check = True
            print(self._check)
            self._connect_count += 1
            print(f"connection : {self._connect_count}")
            utime.sleep_ms(100)
            self._check = False
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # 新しい接続を許可するために再びアドバタイズを開始する．
            self._check = False
            #self._advertise()

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # 新しい接続を許可するために再びアドバタイズを開始する．
            self._check = False
            self._advertise()

        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data
            print(data)

    def set_dev_name(self, name, notify=False, indicate=False):
        fm = '{}si'.format(len(name))
        self._ble.gatts_write(self._handle, struct.pack(fm, name))  # 読み込み可能な書き込み
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # 接続されたセントラルに通知する．
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # 接続されたセントラルに示す．
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_1)

    def _stop1(self, interval_us=None):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_3)
        
    def _stop2(self, interval_us=None):
        self._ble.gap_advertise(interval_us, adv_data=self._payload_4)
        
        
def periph(fn, routedata, _led, mode, timeout):
    ble = bluetooth.BLE()
    
    # gapname = manegement_s1.nameinfo()
    jf_load = ujson.loads(open(fn).read())
    gapname = jf_load["device_number"]
    
    ble.config(gap_name=str(gapname))
    set_name = ble.config('gap_name')
    print(set_name)
    
    print(type(set_name))
    set_name = set_name.decode('utf-8')
    print(type(set_name))

    b = BLE(ble)
    i = 0
    flag = 0
    print(mode)
    
    OPEN = open("data/Routeinfo.json", 'r')
    route = ujson.load(OPEN)
    
    if mode is 0:
        data = str(routedata)
        print(data)
        b._payload_1(jf_load["packet_routeTS"])
        print(timeout)
        print(b._connect_count)
        while timeout > 1 or b._connect_count is 0:
            #if b._check is False and b._connect_count is 0:
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
                utime.sleep(3)
                b._payload_3()
                print("終了")
                _led.off()
                break
            #b._payload_3(jf_load["packet_routeTS"])
            #b.set_dev_name(data, notify=i == 0, indicate=False)
            #print("終了")
            
    if mode is 1:
        print("mode1です")
        data = str(routedata)
        print(data)
        b._payload_1(jf_load["packet_routeTSS"])
        print(timeout)
        print(b._connect_count)
        while timeout > 1 or b._connect_count is 0:
            #if b._check is False and b._connect_count is 0:
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
                utime.sleep(3)
                b._payload_3()
                print("終了")
                _led.off()
                break
            
    if mode is 2:
        if b._check is False and flag == 0:
            #b._payload_1("esp32-3A")
            b._payload_1(route["relay02"])
            while b._check is False and timeout > 0:
                #Write every second, notify every 10 seconds.
                #data = set_name + ',' + str_flag
                #b._name = file["next_1"]
                data = routedata
                i = (i + 1) % 10
                _led.on()
                b.set_dev_name(data, notify=i == 0, indicate=False)
                payload = binascii.hexlify(b._payload_1)
                pay1 = str(binascii.unhexlify(payload), 'utf-8')
                #pay1 = int(binascii.unhexlify(payload), 16)
                print(pay1)
                ##Random walk the temperature.
                print('.')
                utime.sleep_ms(500)
                _led.off()
                utime.sleep_ms(500)
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
            _led.off()
            
        else:
            print("conected")
            print(data)
            _led.off()
            
        print("終了")
        _led.off()
        
if __name__ == "__main__":
    timeout = 10
    routedata = "5"
    fn = 'info/DN02.json'
    red_pin = 13
    _led = machine.Pin(red_pin, machine.Pin.OUT)
    mode = 2
    periph(fn, routedata, _led, mode, timeout)
