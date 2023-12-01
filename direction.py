import RPi.GPIO as GPIO
import time

C1 = 23
C2 = 10
C3 = 17
C4 = 8
C5 = 22
C6 = 25
C7 = 15
C8 = 14
R1 = 7
R2 = 18
R3 = 9
R4 = 24
R5 = 2
R6 = 4
R7 = 3
R8 = 27

rows = [R1, R2, R3, R4, R5, R6, R7, R8]
cols = [C1, C2, C3, C4, C5, C6, C7, C8]

class DirectionMatrices:
    def __init__(self):
        self.down_left = [
    [0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 0],
    [1, 1, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0]
]

# 아래쪽 화살표
        self.up_left = [
    [1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1]
]

# 왼쪽 화살표
        self.down_right = [
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1]
]

# 오른쪽 화살표
        self.up_right = [
    [0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0]
]

        self.x= [
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1]
]


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in range(0,8):
        GPIO.setup(rows[i], GPIO.OUT)
        GPIO.setup(cols[i], GPIO.OUT)
        GPIO.output(rows[i], GPIO.LOW)
        GPIO.output(cols[i], GPIO.HIGH)
    
    direction = DirectionMatrices()
    
    value = 4

    if value == 1:
        pattern = direction.up_left
    elif value == 2:
        pattern = direction.up_right
    elif value == 3:
        pattern = direction.down_left
    elif value == 4:
        pattern = direction.down_right

    
    while(True):
        for i in range(0,8):
            GPIO.output(rows[i], GPIO.HIGH)
            for j in range(0,8):
                if(pattern[i][j]):
                    GPIO.output(cols[j], GPIO.LOW)
                    time.sleep(0.001)
                    GPIO.output(cols[j], GPIO.HIGH)
            GPIO.output(rows[i], GPIO.LOW)
