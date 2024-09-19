import stomp
import stomp.listener
import time

try:
    conn = stomp.Connection()
    conn.set_listener('', stomp.listener.PrintingListener())
    conn.connect(wait=True)
    conn.subscribe(destination='/queue/test', id=int(time.time()))

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    conn.disconnect()