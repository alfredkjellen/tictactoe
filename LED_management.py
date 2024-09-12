# File manages all LED animations
import RPi.GPIO as GPIO
import threading
from time import sleep

GPIO.setmode(GPIO.BCM) # Use Broadcom GPIO pin numbering

# Pin placement:
#  2  3  4
#  7  6  5
#  8  9  10
stop_button_pin = [20, 21, 27] # GPIO inputs that are connected to buttons which stops the animation
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10] # GPIO outputs that are connected to LEDs
stop_animation = False # Stops animation when is set to True

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

def main_animation():
# Gathers all animation functions so that they easier can be exported to 'tictactoe_rasberrypi.py"
    global stop_animation
    while not stop_animation:

        def roulette():
        # Turns on and off all LED pins in the order of the list
            for pin in led_pins:
                if stop_animation:
                    break
                turn_on(pin)
                sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
                turn_off(pin)
            sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
            
        def snake():
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
                if stop_animation:
                        break
                for x in range(CLOCK_START_DIFFERENCE, CLOCK_END_DIFFERENCE ):
                    for i in range(LED_OUTPUTS_MIDDLE_POINT - x, LED_OUTPUTS_MIDDLE_POINT + x, x - 0.5):
                            if stop_animation:
                                    break
                            turn_on(i)
                            sleep(LONGER_SLEEP_TIME_IN_SECONDS)
                            turn_off(i)
            sleep(STANDARD_SLEEP_TIME_IN_SECONDS)
                
        def tic_tac_toe():
        # Writes out TIC TAC TOE 
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
        
        for animation in animations:
            animation()
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