import argparse
import base64
import grpc
import stomp
import stomp.utils
import CalcIMC_pb2
import CalcIMC_pb2_grpc
import time

class AdapterListener(stomp.ConnectionListener):
    def __init__(self, cnn, channel):
        self.cnn = cnn
        self.client = CalcIMC_pb2_grpc.IMCStub(channel)

    # Quando /queue/imc recebe uma mensagem, o broker aciona este método
    def on_message(self, frame):
        request = CalcIMC_pb2.CalculoIMCRequest()
        # Desserializa o objeto
        request.ParseFromString(base64.b64decode(frame.body))
        # Faz a chamada RPC
        response = self.client.CalculoIMC(request)
        # Serializa a resposta
        response_str = response.SerializeToString()
        # Posta a resposta
        self.cnn.send(destination="/queue/tmp", body=base64.b64encode(response_str), content_type="application/octet-stream")

class TestListener(stomp.ConnectionListener):
    def on_message(self, frame):
        response = CalcIMC_pb2.CalculoIMCResponse()
        response.ParseFromString(base64.b64decode(frame.body))
        print(f"Recebido: {response.aviso} (IMC: {response.imc:.2f})")

def adapter(connection):
    channel = grpc.insecure_channel('127.0.0.1:50051')
    # Conexão com o gRPC
    connection.set_listener('adapter', AdapterListener(connection, channel))
    connection.connect(wait=True)
    connection.subscribe(destination='/queue/imc', id=int(time.time()))

def tester(connection):
    connection.set_listener('tester', TestListener())
    connection.connect(wait=True)
    connection.subscribe(destination='/queue/tmp', id=int(time.time()))  # Queue de respostas
    request = CalcIMC_pb2.CalculoIMCRequest(nome='Marta', peso=65.32, altura=1.65)
    connection.send(destination="/queue/imc", body=base64.b64encode(request.SerializeToString()), content_type='application/octet-stream')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", action='store_true')
    args = parser.parse_args()

    cnn = stomp.Connection()  # Conexão com MQ (localhost:61613)
    if args.server:
        adapter(cnn)
    else:
        tester(cnn)
        time.sleep(2)
    cnn.disconect()