import socket
import datetime

# GLOBAL VARIABLES
SERVER = "127.0.0.1"
PORT = 10000
ADDR = (SERVER, PORT)
HEADER = 1024
CLIENTS = []
DISCONNECT_MSG = '!DISCONNECT'

def get_time():
    return (datetime.datetime.now().strftime("%Y.%m.%d."),
            datetime.datetime.now().strftime("%H:%M:%S"),
            datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def handle_client(conn_socket, addr):
    print(f"[+] [NEW CONNECTION - {get_time()[1]}] Client connected from {addr}")

    connected = True
    while connected:
        try:
            msg = conn_socket.recv(HEADER).decode('utf-8')

            match msg:
                case '!DISCONNECT':
                    print(f'[-] [DISCONNECTED - {get_time()[1]}] {addr} disconnected, closing connection')
                    connected = False
                    conn_socket.close()
                case _:
                    print(f"[+] [NEW MESSAGE - {get_time()[1]}] {addr} : {msg}")

        except ConnectionResetError as err:
            print(f"[!] [ERROR - {get_time()[1]}] Client closed connection forcibly or by error - {err.errno}")
            connected  = False
            break

def start():
    print(f"[~] [STARTING - {get_time()[1]}] Server is starting...")
    server.listen()
    print (f"[~] [LISTENING - {get_time()[1]}] Server is listening on {SERVER}:{PORT}")
    while True:
        conn_socket, addr = server.accept()
        handle_client(conn_socket, addr)

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    start()