import os
import sys
import time
import zmq

context = zmq.Context()

# Socket para receber mensagens
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://127.0.0.1:5557")

# Socket para enviar mensagens
sender = context.socket(zmq.PUSH)
sender.connect("tcp://127.0.0.1:5558")

def loop():
    print("Worker ready...")
    while True:
        s = receiver.recv_string()
        # Indicador de progresso simples para o visualizador
        sys.stdout.write('.')
        sys.stdout.flush()
        # Fazer o trabalho
        time.sleep(int(s) * 0.001)
        # Enviar resultados para o Sink
        sender.send(b'')

if os.name == 'nt':
    from zmq.utils.win32 import allow_interrupt
    def interrupted():
        receiver.close()
        sender.close()
        context.destroy()
    with allow_interrupt(interrupted):
        loop()
else:
    loop()