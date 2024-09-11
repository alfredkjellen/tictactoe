# add either readme or short explaination what this file does or server purpose
# all funcitons need function documentation
# all function ideally have some return (true or false)  to say if ok or not
import RPi.GPIO as GPIO
import threading
from time import sleep

GPIO.setmode(GPIO.BCM)  # Jens what is this please explain
GPIO.setwarnings(False) # Jens what is this please explain

# Jens make a ascii art drawing to explain ping 
# x x x
# y y y
# zzz
stop_button_pin = [20, 21, 27] 
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]

GPIO.setup(stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# jens put these "globals" on top and add explaination
stop_animation = False


def reset():
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)

def turn_on(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

def main_animation(): # too big of a funciton max 10-20 rows
    global stop_animation # usuall good to try to avoid globals but I think its needed.. but u can pass it in instead
    while not stop_animation:

        # jens function in a function is nok :) for me or does it needs to be like this
        def roulette():
            for pin in led_pins:
                if stop_animation:
                    break
                turn_on(pin)
                sleep(0.1) # ejensja no magic number proper ROULETTE_SLEEP_TIME_IN_SECONDS = 0.1
                turn_off(pin)
            sleep(0.1)
            
        def snake():
            for i in range(2,11): # no magic numbers
                if stop_animation:
                    break
                turn_on(i)
                sleep(0.1)
            sleep(0.1)
            
            
        def explosion():
            turn_on(6) # ejensja put it in some constant list [6,0,3,4,,1,2,,12,2] where 0 means sleep
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
            #avoid functions within functions
            def bling(start, finnish): # blink bling I dont understand this part
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
                bling(2, 11) # no magic numbers define at top or makea separate file with config or somethinbg
                bling(3, 10)    
            sleep(0.1)

        def clock(): # dont understand this
            def pointer(start, finnish, step):
                 for i in range(start , finnish, step):
                        if stop_animation:
                                break
                        turn_on(i)
                        sleep(0.3)
                        turn_off(i)

            for i in range(2):
                if stop_animation:
                        break
                pointer(2, 11, 4)
                pointer(3, 10, 3)
                pointer(4, 9, 2)
                pointer(5, 8, 1)
            sleep(0.1)

                
        def tic_tac_toe(): # this one is rather clear but not function in funion
            T = [6, 9, 2, 3, 4]
            I = [3, 6, 9]
            C = [4, 3, 2, 5, 8, 9, 10]
            A = [3, 5, 8, 7, 10, 6]
            O = [4, 3, 2, 5, 8, 9, 10, 7]
            E = [2, 5, 8, 9, 10, 6, 7, 3, 4]

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
        
        for a in animations: # dont use a() use something descriptive
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
    while  stop_animation:
        for i in stop_button_pin:
            if GPIO.input(i) == GPIO.HIGH:
                sleep(0.2)
                stop_animation = True

def start_animation():
    global stop_animation
    threading.Thread(target=monitor_stop_button).start()
    main_animation()
    stop_animation = False
