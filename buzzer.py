import RPi.GPIO as GPIO
import time


def buzzerControl(distance, pin):
    for i in range(0,10):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.3)


if __name__ == "__main__":
    buzzer = 1
    GPIO.setmode(GPIO.BCM)  
    GPIO.setwarnings(False)
    GPIO.setup(buzzer, GPIO.OUT)
    buzzerControl( 0, buzzer)
    GPIO.cleanup()
