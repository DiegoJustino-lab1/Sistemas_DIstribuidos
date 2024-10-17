import argparse
import os
import time
import zmq

def printver():
    print(f"Versão da biblioteca nativa: {zmq.zmq_version()}")
    print(f"Versão da biblioteca Python: {zmq.__version__}\n")

def client():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REQ)  # Cliente abre a ponta Request
    socket.connect("tcp://127.0.0.1:5555")

    def loop():
        while True:
            print("Enviando: Hello")
            socket.send_string("Hello")
            msg = socket.recv_string()  # Bloqueante
            print(f"Recebida: {msg}")

    # Apenas para Windows, para capturar corretamente o CTRL-C
    if os.name == 'nt':
        from zmq.utils.win32 import allow_interrupt
        def interrupted():
            socket.close()
            ctx.destroy()
        with allow_interrupt(interrupted):
            loop()
    else:
        loop()

def server():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)  # Servidor abre a ponta Reply
    socket.bind("tcp://127.0.0.1:5555")
    print("Aguardando requisição...")

    def loop():
        while True:
            msg = socket.recv_string()  # Bloqueante
            print(f"Recebido: {msg}\nRespondendo: World!")
            time.sleep(1)
            socket.send_string("World")

    # Apenas para Windows, para capturar corretamente o CTRL-C
    if os.name == 'nt':
        from zmq.utils.win32 import allow_interrupt
        def interrupted():
            socket.close()
            ctx.destroy()
        with allow_interrupt(interrupted):
            loop()
    else:
        loop()

if __name__ == "__main__":
    description = "Apresentação inicial da biblioteca ZeroMQ\nExemplo Request/Reply"
    ap = argparse.ArgumentParser(description=description, epilog="CP117-FACENS/20204")
    ap.add_argument('-s', '--server', action='store_true', help='Roda a aplicação como nodo server')
    args = ap.parse_args()

    printver()
    try:
        if args.server:
            server()
        else:
            client()
    except KeyboardInterrupt:
        pass