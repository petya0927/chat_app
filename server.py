from fileinput import filename
from posixpath import basename
import socket
import datetime
import threading
import time

# GLOBAL VARIABLES
SERVER = "127.0.0.1"
PORT = 10000
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = 'utf-8'
CLIENTS = []
DISCONNECT_MSG = '!DISCONNECT'
FILE_MSG = '!FILE'
SEPARATOR = '<SEPARATOR>'
ACK_MSG = 'ACK'

def get_time():
    return (datetime.datetime.now().strftime("%Y.%m.%d."),
            datetime.datetime.now().strftime("%H:%M:%S"),
            datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def send_to_connections(addr, text):
    message = f'{addr[0]}: {text}'
    for c in CLIENTS:
        c.sendall(message.encode('utf-8'))

def handle_client(conn_socket, addr):
    print(f"[+] [NEW CONNECTION - {get_time()[1]}] Client connected from {addr}")
    CLIENTS.append(conn_socket)

    connected = True
    while connected:
        try:
            message = conn_socket.recv(HEADER).decode(FORMAT)
            conn_socket.send(ACK_MSG.encode(FORMAT))

            match message:
                case '':
                    pass
                case '!DISCONNECT':
                    print(f'[-] [DISCONNECTED - {get_time()[1]}] {addr} disconnected, closing connection')
                    connected = False
                    CLIENTS.remove(conn_socket)
                    conn_socket.close()
                case '!FILE':
                    pass
                case _:
                    print(f"[+] [NEW MESSAGE - {get_time()[1]}] {addr} : {message}")
                    send_to_connections(addr, message)

        except ConnectionResetError as err:
            print(f"[!] [ERROR - {get_time()[1]}] Client closed connection forcibly or by error - {err.errno}")
            connected  = False
            CLIENTS.remove(conn_socket)
            break

def start():
    print(f"[~] [STARTING - {get_time()[1]}] Server is starting...")
    server.listen()
    print (f"[~] [LISTENING - {get_time()[1]}] Server is listening on {SERVER}:{PORT}")
    while True:
        conn_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn_socket, addr))
        thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
start()
