import RPi.GPIO as GPIO
import threading
from time import sleep

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

start_button_pin = 20
stop_button_pin = 21
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]

GPIO.setup(start_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


animation_running = False
stop_animation = threading.Event()



def reset():
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)


def turn_on(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

def start_animation():
    global animation_running
    while True:
        if stop_animation.is_set():
            break
        
        def roulette():
            for pin in led_pins:
                if stop_animation.is_set():
                    break
                turn_on(pin)
                sleep(0.1)
                turn_off(pin)
            sleep(0.1)
            
        def snake():
            for i in range(2,11):
                if stop_animation.is_set():
                    break
                turn_on(i)
                sleep(0.1)
            sleep(0.1)
            
            
        def explosion():
            turn_on(6)
            sleep(0.1)
            turn_on(3)
            turn_on(5)
            turn_on(7)
            turn_on(9)
            sleep(0.1)
            turn_on(2)
            turn_on(4)
            turn_on(8)
            turn_on(10)
            sleep(0.1)
            reset()
            sleep(0.1)
        
        def glitter():
            turn_on(6)
            sleep(0.1)
            turn_off(6)
            turn_on(3)
            turn_on(5)
            turn_on(7)
            turn_on(9)
            sleep(0.1)
            turn_off(3)
            turn_off(5)
            turn_off(7)
            turn_off(9)
            turn_on(2)
            turn_on(4)
            turn_on(8)
            turn_on(10)
            sleep(0.1)
            
            reset()
            sleep(0.1)
            
        animations = [explosion, glitter, snake, roulette]
        
        for a in animations:
            a()
            reset()
                    
    animation_running = False
    
def monitor_start_button():
    global animation_running
    while True:
        if GPIO.input(start_button_pin) == GPIO.HIGH:
            if not animation_running:
                animation_running = True
                stop_animation.clear()
                threading.Thread(target=start_animation).start()
            sleep(0.2)  

def monitor_stop_button():
    global animation_running
    while True:
        if GPIO.input(stop_button_pin) == GPIO.HIGH:
            if animation_running:
                stop_animation.set()
            sleep(0.2)

try:
    
    threading.Thread(target=monitor_start_button).start()
    threading.Thread(target=monitor_stop_button).start()


    while True:
        sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()