import time

import RPi.GPIO as GPIO
import requests


DESTINATION: str = 'http://10.1.5.118:5000'  # server base URL


def on_vibrate(channel):
    print('sending update')
    requests.post(DESTINATION + '/vibrate', json={'washer_id': 0})
    time.sleep(5)


if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(10, GPIO.RISING, callback=on_vibrate)

    input('Press enter to quit\n\n')
    GPIO.cleanup()
