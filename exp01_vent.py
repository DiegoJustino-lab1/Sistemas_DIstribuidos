import zmq
import random
import time
import os

context = zmq.Context()

# Socket para enviar mensagens
sender = context.socket(zmq.PUSH)
sender.bind("tcp://127.0.0.1:5557")

# Socket com acesso direto ao Sink: usado para sincronizar o início do lote
sink = context.socket(zmq.PUSH)
sink.connect("tcp://127.0.0.1:5558")

print("Press Enter when the workers are ready: ")
_ = input()
print("Sending tasks to workers...")

def main():
    try:
        # A primeira mensagem é "0" e sinaliza o início do lote
        sink.send(b'0')

        # Inicializar o gerador de números aleatórios
        random.seed()

        # Enviar 100 tarefas
        total_msec = 0
        for _ in range(100):
            # Carga de trabalho aleatória de 1 a 100 msecs
            workload = random.randint(1, 100)
            total_msec += workload
            sender.send_string(f"{workload}")

        print(f"Total expected cost: {total_msec} msec")
    except KeyboardInterrupt:
        pass
    finally:
        sender.close()
        sink.close()
        context.term()

    # Dar tempo ao ZeroMQ para entregar
    time.sleep(1)

if __name__ == "__main__":
    if os.name == 'nt':
        from zmq.utils.win32 import allow_interrupt
        def interrupted():
            pass
        with allow_interrupt(interrupted):
            main()
    else:
        main()