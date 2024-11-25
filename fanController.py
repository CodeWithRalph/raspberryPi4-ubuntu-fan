import RPi.GPIO as IO
import time
import subprocess

IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(14,IO.OUT)
fanPin = IO.PWM(14,100)
fanPin.start(0)

minTemp = 45
maxTemp = 80
minSpeed = 0
maxSpeed = 100

def get_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not get temperature')
    
def getDutyCycle(currentTemp, tempRange, speedRange):
    tempDiff = tempRange[1] - tempRange[0]
    speedDiff = speedRange[1] - speedRange[0]
    return (speedDiff * (currentTemp - tempRange[0]) / tempDiff) + speedRange[0]

while True:
    currentTemp = get_temp()
    if currentTemp < minTemp:
        currentTemp = minTemp
    elif currentTemp > maxTemp:
        currentTemp = maxTemp
    dutyCycle = int(getDutyCycle(currentTemp, [minTemp, maxTemp], [minSpeed, maxSpeed]))
    fanPin.ChangeDutyCycle(dutyCycle)
    # sleep 10 seconds before doing next cyle
    time.sleep(10)