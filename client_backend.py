import socket
import datetime
from struct import pack
import threading
from IPy import IP
import os

# GLOBAL VARIABLES
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT'
FILE_MSG = '!FILE'
SEPARATOR = '<SEPARATOR>'
ACK_MSG = 'ACK'
HEADER = 1024
received_messages = []
 
def get_time():
    return (datetime.datetime.now().strftime("%Y.%m.%d."),
            datetime.datetime.now().strftime("%H:%M:%S"),
            datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def valid_ip(address):
    try: 
        IP(address)
        return True
    except:
        return False

def send_message(message):
    try:
        # Sending encoded text message
        client.send(message.encode(FORMAT))

        ack_received = False
        while not ack_received:
            try:
                if received_messages[-1] == ACK_MSG:
                    ack_received = True
            except IndexError:
                continue

        return None     # No error occured

    except (ConnectionResetError, ConnectionAbortedError) as err:
        print(f'[!] [EXITING - {get_time()[1]}] Exiting the program due to an error - {err.errno}')
        client.close()
        return err      # Error occured, return with error

def disconnect():
    print(f'[-] [DISCONNECT - {get_time()[1]}] Disconnect from server')
    send_message(DISCONNECT_MSG)        # Sending disconnect message as part of protocol
    client.close()      # Close connection from client side

def receive_message():
    try:
        while True:
            message = client.recv(HEADER).decode(FORMAT)
            if message:
               received_messages.append(message)
    except:
        pass

def connect(ADDR):
    if valid_ip(ADDR[0]):
        print(f'[~] [CONNECTING - {get_time()[1]}] Connecting to {ADDR}')
        try:
            # Connect to given address
            client.connect(ADDR)
            threading.Thread(target=receive_message).start()
            print(f'[+] [CONNECTED - {get_time()[1]}] Connected to {ADDR}')
            return None     # No error occured

        except (ConnectionRefusedError, socket.error) as err:
            print(f'[!] [CONNECTION ERROR - {get_time()[1]}] The connection could not be established with {ADDR}, wrong IP address or target is offline - {err.errno}')
            return err      # Error occured, return with error

    else:
        return 'ip_not_valid'

# Client object create
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)