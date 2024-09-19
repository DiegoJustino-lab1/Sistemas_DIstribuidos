#python
#import xmlrpc.client
#with xmlrpc.client.ServerProxy('http://localhost:50000') as proxy:
#print(proxy.fn_add(4,5))


import argparse
import sys
import xmlrpc.server

parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='para indicar aplicação como servidora')
parser.add_argument('--host', default='localhost')
parser.add_argument('--port', default=50000)

args = parser.parse_args()

Address = args.host
Port = args.port

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
        server.serve_forever()
    except KeyboardInterrupt:
        sys.Exit(0)