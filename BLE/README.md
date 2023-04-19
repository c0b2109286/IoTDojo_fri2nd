# ESP32 BLE通信
## Advertise
### adv.py
【概要】BLEのアドバタイズに関するコード

コード詳細
```python:adv.py
 #service UUID
_Dev_Info_UUID = ubluetooth.UUID(0x180A)
 #Characteristics(UUID,FLAG)
_Dev_CHAR = (ubluetooth.UUID(0x2A7D), ubluetooth.FLAG_READ|ubluetooth.FLAG_WRITE,)
_Dev_SERVICE = (_Dev_Info_UUID, (_Dev_CHAR,),)
```
```python:adv.py
def __init__(self, ble,name):
    #
    ((self._handle,),) = self._ble.gatts_register_services((_Dev_Info_UUID,))
    #
    self._connections = set()
    #
    self._payload = advertising_payload(
        name=name, services=[_Dev_Info_UUID], appearance=0)
```
## Scan
scan.py