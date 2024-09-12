<<<<<<< HEAD
# File manages all LED animations
=======
# add either readme or short explaination what this file does or server purpose
# all funcitons need function documentation
# all function ideally have some return (true or false)  to say if ok or not
>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8
import RPi.GPIO as GPIO
import threading
from time import sleep

<<<<<<< HEAD
GPIO.setmode(GPIO.BCM) # Use Broadcom GPIO pin numbering

# Pin placement:
#  2  3  4
#  7  6  5
#  8  9  10
stop_button_pin = [20, 21, 27] # GPIO inputs that are connected to buttons which stops the animation
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10] # GPIO outputs that are connected to LEDs
stop_animation = False # Stops animation when is set to True
=======
GPIO.setmode(GPIO.BCM)  # Jens what is this please explain
GPIO.setwarnings(False) # Jens what is this please explain

# Jens make a ascii art drawing to explain ping 
# x x x
# y y y
# zzz
stop_button_pin = [20, 21, 27] 
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]
>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8

#CONSTANTS
STANDARD_SLEEP_TIME_IN_SECONDS = 0.1
LONGER_SLEEP_TIME_IN_SECONDS = 0.3

FIRST_LED_PIN = 2
SECOND_LED_PIN = 3
SECOND_TO_LAST_LED_PIN = 10
LAST_LED_PIN = 11

BLINK_LOOP_RANGE = 2
BLINK_REPS = 4
CLOCK_REPS = 2
CLOCK_START_DIFFERENCE = 1.5
CLOCK_END_DIFFERENCE = 5.5
LED_OUTPUTS_MIDDLE_POINT = 6.5


# LED pin setup
GPIO.setup(stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

<<<<<<< HEAD
=======
# jens put these "globals" on top and add explaination
stop_animation = False


>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8
def reset():
# Resets the board
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)

def turn_on(led_pin):
# Turns on selected LED pin
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off(led_pin):
# Turns off selected LED pin    
    GPIO.output(led_pin, GPIO.LOW)

<<<<<<< HEAD
def main_animation():
# Gathers all animation functions so that they easier can be exported to 'tictactoe_rasberrypi.py"
    global stop_animation
    while not stop_animation:

=======
def main_animation(): # too big of a funciton max 10-20 rows
    global stop_animation # usuall good to try to avoid globals but I think its needed.. but u can pass it in instead
    while not stop_animation:

        # jens function in a function is nok :) for me or does it needs to be like this
>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8
        def roulette():
        # Turns on and off all LED pins in the order of the list
            for pin in led_pins:
                if stop_animation:
                    break
                turn_on(pin)
<<<<<<< HEAD
                sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
=======
                sleep(0.1) # ejensja no magic number proper ROULETTE_SLEEP_TIME_IN_SECONDS = 0.1
>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8
                turn_off(pin)
            sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
            
        def snake():
<<<<<<< HEAD
        # Turns on all LED pins in numerical order
            for i in range(FIRST_LED_PIN, LAST_LED_PIN): 
                if stop_animation:
                    break
                turn_on(i)
                sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
            sleep(STANDARD_SLEEP_TIME_IN_SECONDS)

        def blink():
        # Turn on and off all even LED pins, then all odd LED pins four times
            for i in range(BLINK_REPS):
                if stop_animation:
                        break
                for i in range(FIRST_LED_PIN, LAST_LED_PIN, BLINK_LOOP_RANGE):
=======
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
>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8
                    if stop_animation:
                        break
                    turn_on(i)
                sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
                for i in range(FIRST_LED_PIN, LAST_LED_PIN, BLINK_LOOP_RANGE):
                    if stop_animation:
                        break
                    turn_off(i)

                for i in range(SECOND_LED_PIN, SECOND_TO_LAST_LED_PIN, BLINK_LOOP_RANGE):
                    if stop_animation:
                        break
<<<<<<< HEAD
                    turn_on(i)
                sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
                for i in range(SECOND_LED_PIN, SECOND_TO_LAST_LED_PIN, BLINK_LOOP_RANGE):
                    if stop_animation:
                        break
                    turn_off(i)
            sleep(STANDARD_SLEEP_TIME_IN_SECONDS)

        def clock():
        # Rotates through all winning combinations that go through the middle, spinning like a compas
            for i in range(CLOCK_REPS):
=======
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
>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8
                if stop_animation:
                        break
                for x in range(CLOCK_START_DIFFERENCE, CLOCK_END_DIFFERENCE ):
                    for i in range(LED_OUTPUTS_MIDDLE_POINT - x , LED_OUTPUTS_MIDDLE_POINT + x, x - 0.5):
                            if stop_animation:
                                    break
                            turn_on(i)
                            sleep(LONGER_SLEEP_TIME_IN_SECONDS)
                            turn_off(i)
            sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
                
<<<<<<< HEAD
        def tic_tac_toe():
        # Writes out TIC TAC TOE 
=======
        def tic_tac_toe(): # this one is rather clear but not function in funion
>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8
            T = [6, 9, 2, 3, 4]
            I = [3, 6, 9]
            C = [4, 3, 2, 5, 8, 9, 10]
            A = [3, 5, 8, 7, 10, 6]
            O = [4, 3, 2, 5, 8, 9, 10, 7]
            E = [2, 5, 8, 9, 10, 6, 7, 3, 4]

            for letter in "TICTACTOE":
                for LED in letter:
                    if stop_animation:
                            break
                    turn_on(LED)
                    sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
                sleep(LONGER_SLEEP_TIME_IN_SECONDS)
                reset()
                sleep(STANDARD_SLEEP_TIME_IN_SECONDS)    
            
        animations = [roulette, snake, blink, clock, tic_tac_toe]
        
<<<<<<< HEAD
        for animation in animations:
            animation()
=======
        for a in animations: # dont use a() use something descriptive
            a()
>>>>>>> 750db6d4b365e15dab8049aca656cf3114ef34b8
            reset()
    
def tie_animation():
    # Turns of all LED pins during a tie
    for i in range(FIRST_LED_PIN, LAST_LED_PIN):
        turn_off(i)
        sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
    sleep(STANDARD_SLEEP_TIME_IN_SECONDS)

def monitor_stop_button():
    # Checks for an input from one of the stop button pins
    global stop_animation
    while  stop_animation:
        for i in stop_button_pin:
            if GPIO.input(i) == GPIO.HIGH:
                sleep(LONGER_SLEEP_TIME_IN_SECONDS)
                stop_animation = True

def start_animation():
    # Run the main animation while contantly checking for an stop button input
    global stop_animation
    threading.Thread(target=monitor_stop_button).start()
    main_animation()
    stop_animation = False
