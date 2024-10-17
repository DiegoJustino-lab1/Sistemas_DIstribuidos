import grpc
import stomp
import json
import CalcIMC_pb2
import CalcIMC_pb2_grpc

class IMCAdapter(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = CalcIMC_pb2_grpc.IMCServiceStub(self.channel)

    def on_message(self, frame):
        body = json.loads(frame.body)
        nome = body['nome']
        peso = body['peso']
        altura = body['altura']
        response = self.stub.CalculoIMC(CalcIMC_pb2.CalculoIMCRequest(nome=nome, peso=peso, altura=altura))
        reply_to = frame.headers['reply-to']
        self.conn.send(destination=reply_to, body=response.aviso)

def run_adapter():
    conn = stomp.Connection([('localhost', 61613)])
    conn.set_listener('', IMCAdapter(conn))
    conn.connect(wait=True)
    conn.subscribe(destination='/queue/imc', id=1, ack='auto')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        conn.disconnect()

if __name__ == '__main__':
    run_adapter()