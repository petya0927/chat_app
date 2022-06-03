import PySimpleGUI as sg
from client_backend import *

# Get file popup
def get_file():
    sg.theme('black')
    get_file_layout = [
        [
            sg.Text('Choose a file:'),
            sg.In(size=(25, 1), enable_events=True, key='-FILE-'),
            sg.FileBrowse()
        ],
        [
            sg.Button('Send file', enable_events=True, key='-SEND-'),
            sg.Button('Exit', enable_events=True, key='-EXIT-')
        ]
    ]
    get_file_window = sg.Window('Choose a file to send', get_file_layout, element_justification='c')

    while True:
        event, values = get_file_window.read()
        
        if event == '-EXIT-' or event == sg.WIN_CLOSED:
            break

        if event == '-SEND-' and len(values['-FILE-']) > 0:
            # send_file(values['-FILE-'])
            break

    get_file_window.close()


# Get address GUI
def get_address():
    sg.theme('black')
    get_address_layout = [
        [
            sg.Text('IP address:'),
            sg.In(size=(20, 1), enable_events=True, key='-IP-')
        ],
        [
            sg.Text('Port:'),
            sg.In(size=(20, 1), enable_events=True, key='-PORT-')
        ],
        [
            sg.Button('OK', enable_events=True, key='-OK-')
        ]
    ]
    get_address_window = sg.Window('Connect to server', get_address_layout, element_justification='c')
    while True:
        event, values = get_address_window.read()
        
        if event == sg.WIN_CLOSED:
            break

        if event == '-OK-' and len(values['-IP-']) > 0 and len(values['-PORT-']) > 0:
            ADDR = (values['-IP-'], int(values['-PORT-']))
            break

    get_address_window.close()
    return ADDR

ADDR = get_address()

# try to connect
connect_error = connect(ADDR)

# If there is an error
while connect_error != None:
    # an error occured, so show popup
    if sg.popup_yes_no(f'An error occured. Wrong IP address or server is offline.\n\nError: {str(connect_error)}\n\nWould you like to reconnect?') == 'Yes':
        # Client wants to reconnect
        ADDR = get_address()
        connect_error = connect(ADDR)
    else:
        break

# No error occured
else:
    # Chat GUI window create
    sg.theme('black')
    chat_layout = [
        [
            sg.Text('New message:'),
            sg.In(size=(25, 1), enable_events=True, key='-MESSAGE-'),
            sg.Button('Send', enable_events=True, key='-SEND-'),
            sg.Button('File', enable_events=True, key='-FILE-'),
            sg.Button('Exit', enable_events=True, key='-EXIT-')
        ],
        [
            sg.Text(size=(60, 30), background_color='grey18', key='-CHAT-')
        ]
    ]
    chat_window = sg.Window("Client", chat_layout, element_justification='c')
    chat_display = chat_window['-CHAT-']

    # Event loop
    while True:
        received_messages_len = len(received_messages)
        event, values = chat_window.read(timeout=100)

        if len(received_messages) > 0 and len(received_messages) > received_messages_len:
            chat_display.update(chat_display.get() + received_messages[-1] + '\n')

        # Exit button or closing button clicked
        if event == '-EXIT-' or event == sg.WIN_CLOSED:
            disconnect()
            break

        if event == '-FILE-':
            get_file()

        # Send button clicked
        if event == '-SEND-':
            chat_window['-MESSAGE-']('')
            send_error = send_message(values['-MESSAGE-'])
            # Error occured while sending messages
            if send_error != None:
                sg.popup(f'An error occured. Please close this window and reconnect.\n\nError: {str(send_error)}')
                break
        
    chat_window.close()