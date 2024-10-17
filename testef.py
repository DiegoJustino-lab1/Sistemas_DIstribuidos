import stomp
import json
import time

class PrintListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print(f"Received: {frame.body}")

def send_test_message():
    conn = stomp.Connection([('localhost', 61613)])
    conn.set_listener('', PrintListener())
    conn.connect(wait=True)
    conn.subscribe(destination='/queue/tmp', id=1, ack='auto')
    message = {'nome': 'João', 'peso': 70, 'altura': 1.75}
    conn.send(destination='/queue/imc', body=json.dumps(message), headers={'reply-to': '/queue/tmp'})
    time.sleep(2)  # Esperar a resposta
    conn.disconnect()

if __name__ == '__main__':
    send_test_message()