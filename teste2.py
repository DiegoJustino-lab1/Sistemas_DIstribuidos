from os import path, listdir
import argparse
import socket
import threading

parser = argparse.ArgumentParser()

parser.add_argument('--server', action='store_true', help='para indicar aplicação com o servidor')
parser.add_argument('--host', default='localhost')
parser.add_argument('--port', type=int, default=50000)
parser.add_argument('--dir', default='.', help='diretorio com arquivos p servir')
parser.add_argument('file', nargs='?', help='arquivo a ser solicitado')

args = parser.parse_args()

HOST = args.host
PORT = args.port
DIR = args.dir
FILE = args.file

def handle_client(conn, addr):
    print('Conectado por', addr)
    with conn:
        data = conn.recv(128).decode('utf-8').strip()
        file_path = path.join(DIR, data)
        if path.isfile(file_path):
            with open(file_path, 'rb') as f:
                conn.sendall(f.read())
        else:
            conn.sendall(b'Arquivo nao encontrado')

if args.server:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f'Servidor iniciado em {HOST}:{PORT}, servindo arquivos do diretorio {DIR}')
        try:
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr)).start()
        except KeyboardInterrupt:
            print("\nServidor interrompido.")
        finally:
            s.close()
else:
    if FILE:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytearray(FILE[:128], 'utf-8'))
            data = s.recv(65535)
            print(str(data, 'utf-8'))
            s.close()
    else:
        print('Por favor, especifique o arquivo a ser solicitado.')