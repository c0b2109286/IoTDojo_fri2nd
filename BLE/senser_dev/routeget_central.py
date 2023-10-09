import bluetooth
import random
import struct
import utime
import ubinascii
import micropython
import machine
# import manegement_s1
import info
import json

from BLE_advertising import decode_services, decode_name

from micropython import const

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_ADV_SCAN_IND = const(0x02)
_ADV_NONCONN_IND = const(0x03)

# org.bluetooth.service.environmental_sensing
_Dev_Info_UUID = bluetooth.UUID(0x180A)
# org.bluetooth.characteristic.temperature
_Dev_Name_UUID = bluetooth.UUID(0x2A00)
_Dev_CHAR = (_Dev_Name_UUID,bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
_ENV_SENSE_SERVICE = (_Dev_Info_UUID,(_Dev_CHAR,),)


def form_mac_address(addr: bytes) -> str:
    return ":".join('{:02x}'.format(b) for b in addr)

class BLEDevCentral:
    def __init__(self, ble):
        # BLEデバイスのセントラル（中央）としての初期化を行います。
        self._ble = ble
        self._ble.active(True)  # BLEを有効にします。
        self._ble.irq(self._irq)  # BLEの割り込みハンドラーを設定します。

        # 内部状態のリセットを行います。
        self._reset()

    def _reset(self):
        # 成功したスキャンからのキャッシュされた名前とアドレス。
        self._name = None  # デバイス名
        self._addr_type = None  # アドレスタイプ
        self._addr = None  # アドレス

        # キャッシュされた値（あれば）
        self._value = None

        # 各種操作の完了時のコールバック関数。
        # これらは呼び出された後にNoneにリセットされます。
        self._scan_callback = None  # スキャン完了時のコールバック
        self._conn_callback = None  # 接続完了時のコールバック
        self._read_callback = None  # 読み込み完了時のコールバック

        # デバイスからの新しいデータ通知のための永続的なコールバック関数。
        self._notify_callback = None

        # 接続されたデバイス情報
        self._conn_handle = None  # 接続ハンドル
        self._start_handle = None  # 開始ハンドル
        self._end_handle = None  # 終了ハンドル
        self._value_handle = None  # 値ハンドル

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            adv = ubinascii.hexlify(adv_data)
            adr = ubinascii.hexlify(addr)
            # packet = manegement_s1.packetinfo()
            
            jf_open = open("info/SN01.json")
            jf_load = json.load(jf_open)
            packet = jf_load["packet_name"]
            
            #if '6573703332' in adv: #esp32
            #if  '746f736572766572' in adv: #toserver
            if  '746f646576696365' in adv: #todevice
                adv = str(ubinascii.unhexlify(adv), 'utf-8')
                print('type:{} addr:{} rssi:{} data:{}'.format(addr_type, adr, rssi, adv))    
                if adv_type in (_ADV_IND, _ADV_DIRECT_IND) and _Dev_Info_UUID in decode_services(adv_data):
                    # 潜在的なデバイスが見つかり、スキャンを停止します。
                    self._addr_type = addr_type
                    self._addr = bytes(addr)  # 注意: addrバッファは呼び出し元の所有物なので、コピーする必要があります。
                    self._name = adv or "?"
                    self._ble.gap_scan(None)

        elif event == _IRQ_SCAN_DONE:
            print('スキャンが完了しました')
            if self._scan_callback:
                if self._addr:
                    # スキャン中にデバイスが見つかりました（およびスキャンが明示的に停止されました）。
                    self._scan_callback(self._addr_type, self._addr, self._name)
                    print("コールバックは:", self._scan_callback)
                    self._scan_callback = None
                else:
                    # スキャンがタイムアウトしました。
                    self._scan_callback(None, None, None)

        elif event == _IRQ_PERIPHERAL_CONNECT: #gap_connect()が成功しました。
            # 接続成功。
            conn_handle, addr_type, addr = data
            if addr_type == self._addr_type and addr == self._addr:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(self._conn_handle) #characteristicsについて問い合わせる
                print('ペリフェラルが見つかりました')

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # 切断（自分自身またはリモートエンドから開始）。
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                # それが私たちによって開始された場合、既にリセットされています。
                self._reset()

        elif event == _IRQ_GATTC_SERVICE_RESULT:#_ble.gattc_discover_servicesy結果より発生する
            # 接続されたデバイスがサービスを返しました。
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self._conn_handle and uuid == _Dev_Info_UUID:
                self._start_handle, self._end_handle = start_handle, end_handle

        elif event == _IRQ_GATTC_SERVICE_DONE: #上のイベントの検索が完了すると発生する
            # サービスクエリが完了しました。
            if self._start_handle and self._end_handle:
                self._ble.gattc_discover_characteristics(
                    self._conn_handle, self._start_handle, self._end_handle
                )
            else:
                print("環境センシングサービスが見つかりませんでした。")

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            # 接続されたデバイスがキャラクタリスティックを返しました。
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle and uuid == _Dev_Name_UUID:
                self._value_handle = value_handle

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            # キャラクタリスティッククエリの完了。
            if self._value_handle:
                # 接続およびデバイスの検出が完了したら、接続コールバックを実行します。
                if self._conn_callback:
                    self._conn_callback()
            else:
                print("温度キャラクタリスティックが見つかりませんでした。")

        elif event == _IRQ_GATTC_READ_RESULT: #読み込みイベント
            # 読み込みが正常に完了しました。
            conn_handle, value_handle, char_data = data
            if conn_handle == self._conn_handle and value_handle == self._value_handle:
                self._update_value(char_data)
                if self._read_callback:
                    self._read_callback(self._value)
                    #print("12345")
                    #print(self._value)
                    self._read_callback = self._value
                    return self._read_callback

        elif event == _IRQ_GATTC_READ_DONE:
            # 読み込みが完了しました（無効な操作）。
            conn_handle, value_handle, status = data

        elif event == _IRQ_GATTC_NOTIFY:
            # ble_temperature.pyデモは定期的に通知します。
            conn_handle, value_handle, notify_data = data
            if conn_handle == self._conn_handle and value_handle == self._value_handle:
                self._update_value(notify_data)
                if self._notify_callback:
                    self._notify_callback(self._value)

# 接続およびキャラクタリスティックを正常に検出した場合にTrueを返します。
    def is_connected(self):
        return self._conn_handle is not None and self._value_handle is not None

    # 環境センサーサービスを広告しているデバイスを検出します。
    def scan(self, callback=None, scantime = 0):
        self._addr_type = None
        self._addr = None
        self._scan_callback = callback
        self._ble.gap_scan(scantime)

    # スキャンを停止します。
    def not_scan(self):
        self._ble.gap_scan(None)

    # 指定したデバイスに接続します（それ以外の場合、スキャンからキャッシュされたアドレスを使用します）。
    def connect(self, addr_type=None, addr=None, callback=None):
        self._addr_type = addr_type or self._addr_type
        self._addr = addr or self._addr
        self._conn_callback = callback
        if self._addr_type is None or self._addr is None:
            return False
        self._ble.gap_connect(self._addr_type, self._addr) # 接続要求
        return True

    # 現在のデバイスから切断します。
    def disconnect(self):
        if not self._conn_handle:
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()

    # 読み取り要求を発行し、データをコールバックで取得します。
    def read(self, callback):
        if not self.is_connected():
            return
        self._read_callback = callback
        self._ble.gattc_read(self._conn_handle, self._value_handle) # リモート読み込み

    # デバイスから通知を受信したときに呼び出すコールバックを設定します。
    def on_notify(self, callback):
        self._notify_callback = callback

    # データを更新し、データがSint16（16ビットの整数）で、分解能が0.01度セルシウスの温度データである場合に使用します。
    def _update_value(self, data):
        # データはSint16で、温度データは0.01度セルシウスの分解能を持っています。
        self._value = ubinascii.hexlify(data)
        print(type(self._value))
        #self._value = bytes(self._value)
        self._value = ubinascii.unhexlify(self._value)
        print(type(self._value))
        self._value = self._value.replace(b'\x00',b'').decode('utf-8')
        #self._value = self._value.strip()
        return self._value

    # 現在の値を返します。
    def value(self):
        return self._value

    def stop(self):
        if not self._conn_handle:
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()

def Centr():
    # Bluetooth Low Energy（BLE）のインスタンスを作成します。
    ble = bluetooth.BLE()
    
    # BLEデバイス用の中央（Central）クラスを作成します。
    central = BLEDevCentral(ble)

    # デバイスが見つからないフラグを初期化します。
    not_found = False

    # 接続が成功したフラグを初期化します。
    connected = False

    connect_count = 0
    
    SCAN = True

    # BLEデバイスのスキャン結果を処理するコールバック関数
    def on_scan(addr_type, addr, name): # スキャンのコールバック
        if addr_type is not None:
            # デバイス名が"senser01"の場合
            name = ubinascii.hexlify(name)
            addr = ubinascii.hexlify(addr)
            name = str(ubinascii.unhexlify(name), 'utf-8')
            print("デバイスを発見しました:", addr_type, addr, name)
            
            # デバイスに接続します。
            central.connect()
            
            # スキャンを停止します。
            central.not_scan()
        else:
            # デバイスが見つからなかった場合
            nonlocal not_found
            not_found = True
            print("デバイスが見つかりませんでした.")

    # デバイスのスキャンを開始します。
    if connect_count is 0:
        #central.scan(callback=on_scan, scantime = 60000) #60秒
        central.scan(callback=on_scan, scantime= 30000)
    else:
        central.scan(callback=on_scan, scantime = 20000)
        
    # 接続待ち...
    while not central.is_connected():
        utime.sleep_ms(100)
        if not_found:
            return

    print("接続成功")

    # データの読み取りを明示的に実行し、"print"をコールバックとして使用します。
    count = 0
    while count < 1:
        central.read(callback=print)
        print("#####")
        utime.sleep_ms(2000)
        count += 1
        print(count)
    
    # ルートデータを取得します。
    routedata = central._read_callback
    print(routedata)
    
    # 接続を切断します。
    central.disconnect()
    
    jf_open = open('info/SN01.json', 'r')
    jf_load = json.load(jf_open)
    gapname = jf_load["device_number"]
    
    if gapname in routedata:
        if connect_count is 0:
            with open('data/makeroute_data.txt','w',encoding='utf-8')as f:
                print(routedata)
                print(type(routedata))
                f.write(str(routedata))
                f.close()
        else:
            with open('data/makeroute_data.txt','a',encoding='utf-8')as f:
                print(routedata)
                print(type(routedata))
                f.write(str(routedata))
                f.close()
        
    connect_count += 1
    print(connect_count)
    print("切断しました．再接続します")

    return routedata

if __name__ == "__main__":
    Centr()
