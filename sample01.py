from concurrent import futures
import argparse
import grpc
import CalcIMC_pb2
import CalcIMC_pb2_grpc

class CalculoIMC(CalcIMC_pb2_grpc.IMCServicer):
    def CalculoIMC(self, request: CalcIMC_pb2.CalculoIMCRequest, context):
        print(f'received: {request.nome}; {request.peso}; {request.altura}')
        imc = request.peso / (request.altura ** 2)
        if imc < 18.5:
            aviso = "abaixo do peso"
        elif imc < 25.0:
            aviso = "saudável"
        elif imc < 30.0:
            aviso = "com sobrepeso"
        elif imc < 35.0:
            aviso = "obeso"
        elif imc < 40.0:
            aviso = "com obesidade severa"
        else:
            aviso = "com obesidade mórbida"
        return CalcIMC_pb2.CalculoIMCResponse(aviso=f"{request.nome} está {aviso}, IMC={imc:.2f}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    CalcIMC_pb2_grpc.add_IMCServicer_to_server(CalculoIMC(), server)
    server.add_insecure_port("127.0.0.1:50051")
    server.start()
    print("Serving on 127.0.0.1:50051")
    server.wait_for_termination()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', action='store_true')
    args = parser.parse_args()
    if args.server:
        try:
            serve()
        except KeyboardInterrupt:
            pass
    else:
        channel = grpc.insecure_channel('127.0.0.1:50051')
        client = CalcIMC_pb2_grpc.IMCStub(channel)
        res = client.CalculoIMC(CalcIMC_pb2.CalculoIMCRequest(nome="Maria", peso=87.3, altura=1.68))
        print(f"{res.aviso} (IMC: {res.imc:.2f})")