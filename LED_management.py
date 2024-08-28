import RPi.GPIO as GPIO
import threading
from time import sleep

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

stop_button_pin = [20, 21, 27]
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]

GPIO.setup(stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


stop_animation = False


def reset():
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)


def turn_on(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

def main_animation():
    global stop_animation
    while not stop_animation:
        
        def roulette():
            for pin in led_pins:
                if stop_animation:
                    break
                turn_on(pin)
                sleep(0.1)
                turn_off(pin)
            sleep(0.1)
            
        def snake():
            for i in range(2,11):
                if stop_animation:
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

def win_animation():
    turn_off(6)
    
def tie_animation():
    turn_off(2)


def monitor_stop_button():
    global stop_animation
    while True:
        if GPIO.input(stop_button_pin) == GPIO.HIGH:
            stop_animation = True
            break
        sleep(0.2)

def start_animation():
    try:
        threading.Thread(target=monitor_stop_button).start()
        main_animation()


        while True:
            sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()