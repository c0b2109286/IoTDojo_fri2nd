import ubluetooth
import utime
import ubinascii
from micropython import const

_IRQ_SCAN_RESULT                     = const(5)
_IRQ_SCAN_DONE                       = const(6)

ble=ubluetooth.BLE()

if ble.active()== False:
    ble.active(True)#BLEを起動する

# イベント喚起関数irq
def bt_irq(event, data):
    if event == _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, connectable, rssi, adv_data = data
        print('type:{} addr:{} rssi:{} data:{}'.format(addr_type, addr, rssi, ubinascii.hexlify(adv_data)))
    elif event == _IRQ_SCAN_DONE:
        # Scan duration finished or manually stopped.
        print('Scan compelete')
        pass


ble.irq(bt_irq)
# スキャン!!
ble.gap_scan(10000, 30000, 30000,)
