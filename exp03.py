import argparse
import os
import time
import zmq

# Exemplo simples aonde um publisher emite mensagens em 2 tópicos diferentes
# e o cliente subscreve apenas para 1; Note que ZMQ usa comparação byte-a-byte
# para filtrar os tópicos, então a mensagem pode ser 1 única string ou, mais
# correto/recomendado, ser várias mensagens (multipart)

def publisher():
    ctx = zmq.Context.instance()
    s = zmq.Socket = ctx.socket(zmq.PUB)
    s.bind('tcp://127.0.0.1:5558')
    print('Crie os clientes em novos terminais e depois [ENTER] aqui...')
    input()
    # se inverter a ordem de envio (misturar multipart com simples, dá errado)
    s.send_string('topic_aUma mensagem do tópico A')
    s.send(b'topic_b', flags=zmq.SNDMORE)
    s.send_string('Uma mensagem multipart do tópico B')
    # s.send_string('topic_aUma mensagem do tópico A')
    time.sleep(1)

# Este cliente irá receber apenas mensagens do tópico A
def subscriber1():
    ctx = zmq.Context.instance()
    s = zmq.Socket = ctx.socket(zmq.SUB)
    s.connect('tcp://127.0.0.1:5558')
    # Subscribe deve ser após connect.
    s.subscribe('topic_a')
    if os.name == 'nt':
        from zmq.utils.win32 import allow_interrupt
        with allow_interrupt(lambda: ctx.destroy()):
            try:
                msg = s.recv_string()
                # perceba que o tópico não é removido da string/mensagem
                print(f'\n>> Cliente A recebeu: {msg}')
            except KeyboardInterrupt:
                pass

# Este cliente irá receber apenas mensagens do tópico B
def subscriber2():
    ctx = zmq.Context.instance()
    s = zmq.Socket = ctx.socket(zmq.SUB)
    s.connect('tcp://127.0.0.1:5558')
    # Subscribe deve ser após connect
    s.setsockopt(zmq.SUBSCRIBE, b'topic_b')
    if os.name == 'nt':
        from zmq.utils.win32 import allow_interrupt
        with allow_interrupt(lambda: ctx.destroy()):
            try:
                # Note que as mensagens do tópico B são multipart!
                _ = s.recv() # recebe tópico
                msg = s.recv_string() # recebe mensagem
                print(f'\n>> Cliente B recebeu: {msg}')
            except KeyboardInterrupt:
                pass

# Este cliente irá receber ambos os tópicos. Note um problema com o protocolo
# se inverter a sequência (topic_b antes de topic_a) a lógica quebra.
def subscriber3():
    ctx = zmq.Context.instance()
    s = zmq.Socket = ctx.socket(zmq.SUB)
    s.connect('tcp://127.0.0.1:5558')
    s.setsockopt(zmq.SUBSCRIBE, b'')
    if os.name == 'nt':
        from zmq.utils.win32 import allow_interrupt
        with allow_interrupt(lambda: ctx.destroy()):
            try:
                print('\n>> Cliente C recebeu:')
                print(s.recv_string())  # topic_a
                print(s.recv())  # topic_b part 1
                print(s.recv_string())  # topic_b part 2
                print('\n<< -----')
            except KeyboardInterrupt:
                pass

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--client', type=int, choices=range(1, 4))
    args = ap.parse_args()
    if args.client:
        match args.client:
            case 1:
                subscriber1()
            case 2:
                subscriber2()
            case 3:
                subscriber3()
    else:
        publisher()
