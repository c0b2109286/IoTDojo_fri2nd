import bluetooth
import time

ble=ubluetooth.BLE()
# macアドレスを十六進数で表示
def form_mac_address(addr: bytes) -> str:
    return ":".join('{:02x}'.format(b) for b in addr)

if ble.active()== True:
    ble.active(False)#BLEをオフ

    print(ble.active())
    #macアドレスを表示する
    print("BLE current mac address: {}".format(form_mac_address(ble.config("mac"))))