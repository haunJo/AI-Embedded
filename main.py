import sys
sys.path.append('./')

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import cv2
from picamera import PiCamera
import time
from PIL import Image
import RPi.GPIO as GPIO
from direction import DirectionMatrices
from led import ledControl
from buzzer import buzzerControl
from pycoral.utils import edgetpu
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.adapters import segment
C1 = 23
C2 = 4
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
R6 = 10
R7 = 3
R8 = 27

led = 11
buzzer = 1

rows = [R1, R2, R3, R4, R5, R6, R7, R8]
cols = [C1, C2, C3, C4, C5, C6, C7, C8]


def load_model_tpu(model_path):
    interpreter = edgetpu.make_interpreter(model_path)
    interpreter.allocate_tensors()
    return interpreter


# Tflite 모델 로드 함수
def load_model(model_path):
    interpreter = tflite.Interpreter(model_path = model_path)
    interpreter.allocate_tensors()
    return interpreter

def GPIOinit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in range(0,8):
        GPIO.setup(rows[i], GPIO.OUT)
        GPIO.setup(cols[i], GPIO.OUT)
        GPIO.output(rows[i], GPIO.LOW)
        GPIO.output(cols[i], GPIO.HIGH)
    GPIO.setup(led, GPIO.OUT)
    pwm_led = GPIO.PWM(led, 100)
    GPIO.setup(buzzer, GPIO.OUT)
    return pwm_led


def clear_pin():
    for i in range(0,8):
        GPIO.output(rows[i], GPIO.LOW)
        GPIO.output(cols[i], GPIO.HIGH)

def draw_arrow_on_matrix(period_, direction , value  ):
    if value == 0:
        pattern = direction.up_left
    elif value == 1:
        pattern = direction.up_right
    elif value == 2:
        pattern = direction.down_right
    elif value == 3:
        pattern = direction.down_left
    elif value == 4:
        pattern = direction.x
    period = period_
    start_time = time.time()
    while( time.time() - start_time < period):
        for i in range(0,8):
            GPIO.output(rows[i], GPIO.HIGH)
            for j in range(0,8):
                if(pattern[i][j]):
                    GPIO.output(cols[j], GPIO.LOW)
                    time.sleep(0.001)
                    GPIO.output(cols[j], GPIO.HIGH)
            GPIO.output(rows[i], GPIO.LOW)

def Predict_position(image):
    return 0



if __name__ == "__main__":
    direction = DirectionMatrices()

    print("-----GPIO Setting-----")
    LED = GPIOinit()
    LED.start(0)
    print("Done")
    
    print("LED test")
    for i in range(0,100):
        ledControl(i, LED)
    print("Done")
    
    print("Buzzer test")
    buzzerControl(0, buzzer)
    print("Done")
    # 모델 로드
    #interpreter = load_model('test.tflite')
    interpreter = load_model_tpu('test_edgetpu.tflite')
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    #print(input_details)
    height = input_details[0]['shape'][2]
    width = input_details[0]['shape'][3]


    width, height = common.input_size(interpreter)
    print(height, width)
    
    half_width = width // 2
    half_height = 960 // 2


    print("8*8 Dot Matrix test")
    for k in range(0,15):
    draw_arrow_on_matrix(0.1, direction, k % 5)
    print("Done")


    ## 카메라 실행
    with PiCamera() as camera:
        camera.resolution = (640, 480) 
        new_output = np.empty((480, 640,3), dtype = np.uint8)
        taken_time = time.time()
        camera.start_preview()
        while True:
            camera.capture(new_output, 'bgr')
            cv2.imshow('frame', new_output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if (time.time() - taken_time > 1):
                taken_time = time.time()
                #cpu
                #output = cv2.resize(output, (width, height))
                #output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                #output = np.expand_dims(output.astype('float32') / 255.0, axis = 0)
                #output = np.transpose(output, (0,3,1,2))
                
                #tpu
                output = cv2.cvtColor(new_output, cv2.COLOR_BGR2RGB)
                output = cv2.resize(output.astype('float32') / 255.0, (960, 544))
                output = np.transpose(output, (2,0,1))
                print(output)
                common.set_input(interpreter, output)
                pre_time = time.time() - taken_time
                print("preprocess : ",pre_time)
                interpreter.invoke()
                print("predict : " , time.time() - pre_time - taken_time)
                result = segment.get_output(interpreter)
                
                up_left = result[:, :half_width, :half_height]
                up_right = result[:, :half_width, half_height:]
                down_left = result[:, half_width:, :half_height]
                down_right= result:, half_width2:, half_hegith:]

                size = [np.sum(up_left), np.sum(up_right), np.sum(down_left), np.sum(down_right)]
                
                index = size.index(max(size))
                
                if size[index] > 60000:
                    buzzerControl(0, buzzer)
                    draw_arrow_on_matrices(3, direction, index)
                else:
                    draw_arrow_on_matrices(3, direction, 4)
                #이미지 처리
                #예측
                #interpreter.set_tensor(input_details[0]['index'], output)
                #interpreter.invoke()
                #output_data = interpreter.get_tensor(output_details[0]['index'])
                #print(output_data.shape)
                new_output = np.empty((480, 640,3), dtype = np.uint8)
        camera.stop_preview()
        cv2.destroyAllWindows()


            

