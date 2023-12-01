import RPi.GPIO as GPIO
import time


def ledControl(distance, pin):
    duty = distance
    
    try:
        pin.ChangeDutyCycle(float(duty))  # PWM 듀티 사이클 변경: LED 켜기
        time.sleep(0.05)
    except KeyboardInterrupt:
        exit(1)

    pin.ChangeDutyCycle(0)


if __name__ == "__main__":
    gpio = 11
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio, GPIO.OUT)
    pwm_led = GPIO.PWM(gpio, 100)
    pwm_led.start(0)

    for i in range(0,100):
        ledControl(i, pwm_led)

    pwm_led.ChangeDutyCycle(0.0)
    pwm_led.stop()
    GPIO.cleanup()
