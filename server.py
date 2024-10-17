import stomp
import json
import numpy as np
from numpy import percentile

class TukeyRequestListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        data = np.asarray(json.loads(frame.body))
        quartiles = percentile(data, [25, 50, 75])
        tid = self.conn.begin()
        self.conn.send(destination='/queue/median', body=str(quartiles[1]), transaction=tid)
        self.conn.send(destination='/queue/first-q', body=str(quartiles[0]), transaction=tid)
        self.conn.send(destination='/queue/third-q', body=str(quartiles[2]), transaction=tid)
        self.conn.send(destination='/queue/min', body=str(data.min()), transaction=tid)
        self.conn.send(destination='/queue/max', body=str(data.max()), transaction=tid)
        self.conn.commit(tid)

def run_server():
    conn = stomp.Connection([('localhost', 61613)])
    conn.set_listener('', TukeyRequestListener(conn))
    conn.connect(wait=True)
    conn.subscribe(destination='/queue/tukey', id=1, ack='auto')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        conn.disconnect()

if __name__ == '__main__':
    run_server()