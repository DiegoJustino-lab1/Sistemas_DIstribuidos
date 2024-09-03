#download por: python -m venv .venv
import argparse
import socket 

parse = argparse.ArgumentParser()
parse.add_argument('--server', action= 'store_true', help='Para Iniciar')
parse.add_argument('--host', default= 'localhost')
parse.add_argument('--port', default= 50000)
parse.add_argument('--msg', default= 'Hello World', help='Mensagem a ser enviada')

args = parse.parse_args()

HOST = args.host
PORT = args.port
MSG = args.msg

if args.server:
    with socket.socket() as s:
        s.blind(HOST, PORT)
        s.listen(1)
        conn, addr = s.accept
        with conn:
            print('Conected by', addr)
            while True:
                    data= conn.recv(152)
                    if not data: break
                    msg = str(data, 'utf-8')
                    conn.sendall(bytearray(msg.upper(), 'uft-8'))
else:
        with socket.socket() as s:
              s.connect((HOST, PORT))
              s.sendall(bytearray(MSG[:128], 'utf-8'))
              data = s.recv(152)
              print(str(data, 'utf-8'))
              s.close()
                    