import argparse
import json
import stomp
import stomp.listener
import time
import numpy as np
from numpy import percentile
from numpy.random import rand

class TukeyRequestListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        data = np.asarray(json.loads(frame.body))
        quartiles = percentile(data, [25, 50, 75])
        tid = self.conn.begin()
        self.conn.send(destination='/queue/median', body=str(quartiles[1]))
        self.conn.send(destination='/queue/first-q', body=str(quartiles[0]))
        self.conn.send(destination='/queue/third-q', body=str(quartiles[2]))
        self.conn.send(destination='/queue/min', body=str(data.min()))
        self.conn.send(destination='/queue/max', body=str(data.max()))
        self.conn.commit(tid)

class TukeyResponseListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        print(f"{frame.headers['destination']}: {frame.body}")

def adapter(connection):
    connection.set_listener('adapter', TukeyRequestListener(connection))
    connection.connect(wait=True)
    connection.subscribe(destination='/queue/tukey', id=int(time.time()))

def tester(connection):
    connection.set_listener('tester', TukeyResponseListener(connection))
    connection.connect(wait=True)
    connection.subscribe(destination='/queue/median', id=int(time.time()))
    connection.subscribe(destination='/queue/first-q', id=int(time.time()))
    connection.subscribe(destination='/queue/third-q', id=int(time.time()))
    connection.subscribe(destination='/queue/min', id=int(time.time()))
    connection.subscribe(destination='/queue/max', id=int(time.time()))
    data = rand(25)
    print(f"Data: {data}")
    connection.send(destination='/queue/tukey', body=json.dumps(data.tolist()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", action='store_true')
    args = parser.parse_args()

    conn = stomp.Connection()  # Conexão com MQ (localhost:61613)
    if args.server:
        adapter(conn)
    else:
        tester(conn)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        conn.disconnect()