import machine
import utime

def blink_rgb_led(red_pin, green_pin, blue_pin, duration=5):
    red_led = machine.Pin(red_pin, machine.Pin.OUT)
    green_led = machine.Pin(green_pin, machine.Pin.OUT)
    blue_led = machine.Pin(blue_pin, machine.Pin.OUT)
    
    red_led.off()  # 終了時にLEDを消灯
    green_led.off()
    blue_led.off()
    
    try:
        for _ in range(int(duration / 0.5)):  # 0.5秒ごとに点滅

            green_led.on()  # 緑LEDを点灯
            utime.sleep(0.5)  # 0.5秒待つ
            green_led.off()  # 緑LEDを消灯

            blue_led.on()  # 青LEDを点灯
            utime.sleep(0.5)  # 0.5秒待つ
            blue_led.off()  # 青LEDを消灯
            
            red_led.on()  # 青LEDを点灯
            utime.sleep(0.5)  # 0.5秒待つ
            red_led.off() 
            
            
    finally:
        red_led.off()  # 終了時にLEDを消灯
        green_led.off()
        blue_led.off()

# RGB LEDの各色のピン番号を設定して関数を呼び出す

blink_rgb_led(13, 14, 15)
