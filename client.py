import stomp
import json
import time
import numpy as np
from numpy.random import rand

class PrintListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print(f"{frame.headers['destination']}: {frame.body}")

def send_test_message():
    conn = stomp.Connection([('localhost', 61613)])
    conn.set_listener('', PrintListener())
    conn.connect(wait=True)
    conn.subscribe(destination='/queue/median', id=1, ack='auto')
    conn.subscribe(destination='/queue/first-q', id=2, ack='auto')
    conn.subscribe(destination='/queue/third-q', id=3, ack='auto')
    conn.subscribe(destination='/queue/min', id=4, ack='auto')
    conn.subscribe(destination='/queue/max', id=5, ack='auto')

    data = rand(25).tolist()
    message = json.dumps(data)
    conn.send(destination='/queue/tukey', body=message, headers={'reply-to': '/queue/tmp'})
    time.sleep(5)  # Esperar a resposta
    conn.disconnect()

if __name__ == '__main__':
    send_test_message()