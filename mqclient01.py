import stomp
import time

conn = stomp.Connection()
conn.set_listener('', stomp.PrintingListener())
conn.connect(wait=True)
conn.subscribe(destination='/queue/test', id=int(time.time()))

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    conn.disconnect()