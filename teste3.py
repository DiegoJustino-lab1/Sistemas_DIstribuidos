import argparse
import sys
import xmlrpc.server

parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='para indicar aplicação como servidora')
parser.add_argument('--host', default='localhost')
parser.add_argument('--port', type=int, default=50000)

args = parser.parse_args()

Address = args.host
Port = args.port

if args.server:
    with xmlrpc.server.SimpleXMLRPCServer((Address, Port)) as server:
        server.register_introspection_functions()
        server.register_multicall_functions()
    
        @server.register_function()
        def fn_add(a, b):
            return a + b
    
        @server.register_function()
        def fn_sub(a, b):
            return a - b
    
        @server.register_function()
        def fn_mul(a, b):
            return a * b
    
        @server.register_function()
        def fn_div(a, b):
            return a / b
    
        try:
            print(f"Servidor XML-RPC iniciado em {Address}:{Port}")
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor interrompido.")
            sys.exit(0)
else:
    import xmlrpc.client
    with xmlrpc.client.ServerProxy(f'http://{Address}:{Port}') as proxy:
        print()
        print(f"4 + 5 = {proxy.fn_add(4, 5)}")
        print(f"4 - 5 = {proxy.fn_sub(4, 5)}")
        print(f"4 * 5 = {proxy.fn_mul(4, 5)}")
        print(f"4 / 5 = {proxy.fn_div(4, 5)}")