import RPi.GPIO as GPIO
from time import sleep
import time

motionPin12 = 12
redPin37 = 37
greenPin35 = 35

trigPin40 = 40
echoPin38 = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motionPin12, GPIO.IN)
GPIO.setup(trigPin40, GPIO.OUT)
GPIO.setup(echoPin38, GPIO.IN)

sleep(10)
GPIO.setup(greenPin35, GPIO.OUT)
GPIO.setup(redPin37, GPIO.OUT)
greenMod = GPIO.PWM(greenPin35, 50)
redMod = GPIO.PWM(redPin37, 50)

greenMod.start(1)
redMod.start(1)


def echolocate():
    GPIO.output(trigPin40, 0)
    sleep(2E-6)
    GPIO.output(trigPin40, 1)
    sleep(10E-6)
    GPIO.output(trigPin40, 0)

    while GPIO.input(echoPin38) == 0:
        pass
    echoStartTime = time.time()

    while GPIO.input(echoPin38) == 1:
        pass
    
    echoStopTime = time.time()
    pingTravelTime = echoStopTime - echoStartTime
    #print(int(pingTravelTime*1E6))
    distance = (pingTravelTime*1E6/2)*0.0132
    print(f"Distance: {round(distance, 2)}")
    time.sleep(.2)
    
    return distance


try:
    while True:
        motion = GPIO.input(motionPin12)
        distance = echolocate()

        if motion == 1 and distance>19:
            greenMod.ChangeFrequency(2)
            greenMod.ChangeDutyCycle(50)
            GPIO.output(redPin37, 0)
            redMod.ChangeDutyCycle(0)
            #GPIO.output(greenPin35, 0)
        # No motion detected
        if motion == 0:
            #GPIO.output(redPin37, 0)
            #GPIO.output(greenPin35, 1)
            greenMod.ChangeFrequency(50)
            redMod.ChangeDutyCycle(0)
            greenMod.ChangeDutyCycle(50)


        if distance < 20 and distance > 6 and motion == 1:
            greenMod.ChangeFrequency(50)
            redMod.ChangeFrequency(50)
            greenPercentage = distance*7 -41
            redPercentage = 99 - greenPercentage
            print(f'Green percentage: {greenPercentage}')
            print(f'Red percentage: {redPercentage}')
            greenMod.ChangeDutyCycle(greenPercentage)
            redMod.ChangeDutyCycle(redPercentage)

        if distance < 7 and motion == 1:
            greenMod.ChangeDutyCycle(0)
            GPIO.output(greenPin35, 0)
            redMod.ChangeDutyCycle(50)
            redMod.ChangeFrequency(10)

            
        
        print(motion)
        #print(greenFreq)
        sleep(.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nadios")
