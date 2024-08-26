import RPi.GPIO as GPIO
import threading
import time

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

start_button_pin = 20
stop_button_pin = 21
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]

GPIO.setup(start_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


animation_running = False
stop_animation = threading.Event()

def start_animation():
    global animation_running
    while True:
        if stop_animation.is_set():
            break
        for pin in led_pins:
            if stop_animation.is_set():
                break
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)
    animation_running = False

def monitor_start_button():
    global animation_running
    while True:
        if GPIO.input(start_button_pin) == GPIO.LOW: 
            if not animation_running:
                animation_running = True
                stop_animation.clear()
                threading.Thread(target=start_animation).start()
            time.sleep(0.2)  

def monitor_stop_button():
    global animation_running
    while True:
        if GPIO.input(stop_button_pin) == GPIO.LOW: 
            if animation_running:
                stop_animation.set()
            time.sleep(0.2)

try:
    
    threading.Thread(target=monitor_start_button).start()
    threading.Thread(target=monitor_stop_button).start()


    while True:
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
