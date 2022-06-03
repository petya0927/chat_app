import socket
import datetime
import time

# GLOBAL VARIABLES
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT'

def get_server_address():
    server = input('SERVER IP ADDRESS (leave blank to use default: 127.0.0.1): ') or '127.0.0.1'
    port = int(input('SERVER PORT (leave blank to use default: 10000): ') or '10000')
    return (server, port)

def get_time():
    return (datetime.datetime.now().strftime("%Y.%m.%d."),
            datetime.datetime.now().strftime("%H:%M:%S"),
            datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def send_message():
    while True:
        try:
            print('New message:', end=' ')
            message = input()
            client.send(message.encode('utf-8'))

        except (KeyboardInterrupt) as err:
            client.send(DISCONNECT_MSG.encode('utf-8'))
            print(f'[!] [EXITING - {get_time()[1]}] Exiting the program due to keyboard interruption in 10s')
            time.sleep(10)
            client.close()
            exit()

        except (ConnectionResetError, ConnectionAbortedError) as err:
            print(f'[!] [EXITING - {get_time()[1]}] Exiting the program due to an error in 10s - {err.errno}')
            time.sleep(10)
            client.close()
            exit()

if __name__ == '__main__':
    ADDR = get_server_address()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'[~] [CONNECTING - {get_time()[1]}] Connecting to {ADDR}')
    for attempt in range(1, 11):
        try:
            client.connect(ADDR)
            print(f'[+] [CONNECTED - {get_time()[1]}] Connected to {ADDR}')
            break
        except ConnectionRefusedError as err:
            print(f'[!] [CONNECTION ERROR - {get_time()[1]}] The connection could not be established with {ADDR}, wrong IP address or target is offline - {err.errno}')
            print(f'[~] [RETRY CONNECTING - {get_time()[1]}] Retrying establish connection to {ADDR}, attempt #{attempt}.')
            continue
    
    else:
        print(f'[!] [EXITING - {get_time()[1]}] Exiting the program due to an error in 10s')
        time.sleep(10)
        client.close()
        exit()

    send_message()
        