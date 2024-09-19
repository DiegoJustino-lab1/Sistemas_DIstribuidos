import CalcIMC_pb2 as CalcIMC

request = CalcIMC.CalculoIMCRequest()
request.nome = "Marcos"
request.peso = 107.5
request.altura = 1.78
print(request.SerializeToString())