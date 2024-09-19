import os
import argparse
import socket
import threading

# Configuração dos argumentos da linha de comando
parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='para indicar aplicação como servidora')
parser.add_argument('--host', default='localhost')
parser.add_argument('--port', type=int, default=50000)
parser.add_argument('--dir', default='.', help='diretório com arquivos para servir (ignorada se cliente)')
parser.add_argument('--file', default='/', help='arquivo para puxar (ignorada se servidor)')
args = parser.parse_args()

HOST = args.host
PORT = args.port
DIR = args.dir
FILE = args.file

# Verificação rápida do argumento
if args.server and not os.path.isdir(DIR):
    print("Caminho especificado não é um diretório!")
    exit(1)

def handle_client(conn, addr):
    print(f'Conectado por {addr}')
    data = conn.recv(128).decode('utf-8').strip()
    req = data.split()
    
    if len(req) < 2 or req[0] != 'GET':
        conn.sendall(b'400 Bad Request\n\n')
        conn.close()
        return
    
    if req[1] == '/':
        file_list = '\n'.join(os.listdir(DIR))
        response = f'200 OK\n\n{file_list}'
        conn.sendall(response.encode('utf-8'))
    else:
        file_path = os.path.join(DIR, req[1].lstrip('/'))
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                file_data = f.read()
                response = f'200 OK\nLength: {len(file_data)}\n\n'.encode('utf-8') + file_data
                conn.sendall(response)
        else:
            conn.sendall(b'404 Nao encontrado\n\n')
    conn.close()

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
            s.sendall(f'GET {FILE}\n'.encode('utf-8'))
            data = s.recv(65535)
            print(data.decode('utf-8'))