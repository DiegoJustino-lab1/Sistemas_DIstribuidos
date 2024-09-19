import grpc
from concurrent import futures
import CalcIMC_pb2
import CalcIMC_pb2_grpc

class CalcIMCServicer(CalcIMC_pb2_grpc.CalcIMCServicer):
    def CalcularIMC(self, request, context):
        imc = request.peso / (request.altura ** 2)
        mensagem = "IMC calculado com sucesso"
        return CalcIMC_pb2.CalculoIMCResponse(mensagem=mensagem, imc=imc)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CalcIMC_pb2_grpc.add_CalcIMCServicer_to_server(CalcIMCServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor rodando na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()