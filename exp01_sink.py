import os
import sys
import time
import zmq

context = zmq.Context()

# Socket para receber mensagens
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://127.0.0.1:5558")

def main():
    print("Sink waiting for batch...")
    try:
        # Esperar pelo início do lote
        _ = receiver.recv()

        # Iniciar nosso relógio agora
        tstart = time.time()

        # Processar 100 confirmações
        for task_nbr in range(100):
            _ = receiver.recv()
            if task_nbr % 10 == 0:
                sys.stdout.write(':')
            else:
                sys.stdout.write('.')
            sys.stdout.flush()

        # Calcular e relatar a duração do lote
        tend = time.time()
        print(f"\nTotal elapsed time: {(tend - tstart) * 1000} msec")
    except KeyboardInterrupt:
        pass
    finally:
        receiver.close()
        context.term()

if os.name == 'nt':
    from zmq.utils.win32 import allow_interrupt
    def interrupted():
        pass
    with allow_interrupt(interrupted):
        main()
else:
    main()