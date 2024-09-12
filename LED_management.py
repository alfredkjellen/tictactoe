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

        def blink():
            def bling(start, finnish):
                for i in range(start, finnish, 2):
                    if stop_animation:
                        break
                    turn_on(i)
                sleep(0.1)
                for i in range(start, finnish, 2):
                    if stop_animation:
                        break
                    turn_off(i)

            for i in range(4):
                if stop_animation:
                        break
                bling(2, 11)
                bling(3, 10)    
            sleep(0.1)

        def clock():
            def pointer(start, finnish, step):
                for i in range(start , finnish, step):
                        if stop_animation:
                                break
                        turn_on(i)
                sleep(0.3)
                for i in range(start , finnish, step):
                        if stop_animation:
                                break
                        turn_off(i)
            for i in range(2):
                if stop_animation:
                        break
                pointer(2, 11, 4)
                pointer(3, 10, 3)
                pointer(4, 9, 2)
                pointer(5, 8, 1)
            sleep(0.1)

                
        def tic_tac_toe():
            T = [6, 9, 2, 3, 4]
            I = [3, 6, 9]
            C = [4, 3, 2, 7, 8, 9, 10]
            A = [3, 7, 8, 5, 10, 6]
            O = [4, 3, 2, 7, 8, 9, 10, 5]
            E = [2, 7, 8, 9, 10, 6, 5, 3, 4]

            def letter(letter):
                for LED in letter:
                    if stop_animation:
                            break
                    turn_on(LED)
                    sleep(0.1)
                sleep(0.3)
                reset()
                sleep(0.1)    

            letter(T)
            letter(I)
            letter(C)
            letter(T)
            letter(A)
            letter(C)
            letter(T)
            letter(O)
            letter(E)
            
        animations = [explosion, roulette, glitter, snake, blink, clock, tic_tac_toe]
        
        for a in animations:
            a()
            reset()

def win_animation():
    turn_off(6)
    
def tie_animation():
    for i in range(2,11):
        turn_off(i)
        sleep(0.1)
    sleep(0.1)
            


def monitor_stop_button():
    global stop_animation
    while not stop_animation:
        for i in stop_button_pin:
            if GPIO.input(i) == GPIO.HIGH:
                sleep(0.2)
                stop_animation = True

def start_animation():
    global stop_animation
    threading.Thread(target=monitor_stop_button).start()
    main_animation()
    stop_animation = False