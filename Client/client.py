#!/usr/bin/env python3

# Client-side for the server.py program

import socket
import os

HOST = '127.0.0.1'
PORT = 5412

BUFFER_SIZE = 1024
ENCODING = 'utf-8'


def main():
    """
    This function will create a socket, connect to the server, and send a message.
    """
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to the server
        sock.connect((HOST, PORT))
        connected = True
        while connected:
            # Get the message from the server
            server_message = sock.recv(BUFFER_SIZE).decode(ENCODING).lower()
            # Display the message from the server to the client
            if server_message == 'exit':
                connected = False
            elif server_message == 'channel':
                handle_channel(sock)
            elif server_message == 'what':
                handle_what(sock)
            elif server_message == 'size':
                handle_write(sock)
            elif server_message == 'read':
                handle_read(sock)
            elif server_message == 'empty':
                print('No notes in this Directory')
                input()
                handle_what(sock)
            else:
                handle_invalid_what(sock)
                


def handle_channel(sock):
    """
    This function will handle the channel message.
    """
    client_message = input(
        'Please enter a channel: python(PY), software testing(QA), or database(DB).')
    sock.sendall(client_message.encode(ENCODING))


def handle_what(sock):
    """
    This function will handle the what message.
    """
    client_message = input('Would you like to Write(WRIT), Read, Channel(Chan) or Quit?\n')
    sock.sendall(client_message.encode(ENCODING))


def handle_invalid_what(sock):
    """
    This function will handle the invalid what message.
    """
    client_message = input('Please enter a valid command: Read, WRIT, Quit, or Chan \n')
    sock.sendall(client_message.encode(ENCODING))


def handle_write(sock):
    """
    This function will handle the write message.
    """
    upload = input('Would you like to upload a file? Y/N:')
    if upload == 'Y' or upload == 'y':
        handle_send_from_file(sock)
    elif upload == 'N' or upload == 'n':
        content = input('Please enter the note: ')
        file_name = input('Please enter a file_name for the note: ')
        note = f'{file_name}<BOF>{content}'
        sock.sendall(f'{note.__sizeof__()}'.encode(ENCODING))
        sock.sendall(note.encode(ENCODING))
    else:
        print('Invalid input')
        handle_write(sock)
    


def handle_send_from_file(sock):
    """
    This function will handle the write message.
    """
    file_path = input('Please enter the file path: ')
    try:
        with open(os.path.relpath(file_path), 'rb') as file:
            content = file.read()
            note = f'{file_path}<BOF>{content}'
            sock.sendall(f'{note.__sizeof__()}'.encode(ENCODING))
            sock.sendall(note.encode(ENCODING))
    except FileNotFoundError:
        input('File not found. Press enter to continue.')
        handle_send_from_file(sock)



def handle_read(sock):
    """
    Writes the recieved notes to a file and spceifies the file location. 
    Also prints the notes to the console
    """
    notes = ''
    while True:
        stream = sock.recv(BUFFER_SIZE).decode(ENCODING)
        notes += stream
        if stream.endswith('<EOT>') or stream == 'EmptyWhat':
            sock.sendall('Received'.encode(ENCODING))
            notes = notes.replace('<EOT>', '')
            break
    if notes == 'EmptyWhat':
        print('No notes found')
        input()
        handle_what(sock)
    else:
        notes = notes.split('<EOF>')
        for note in notes:
            if note == '':
                continue
            file_name, file_content = note.split('<BOF>')

            print(file_content)
            filename = file_name.split('/')[1]
            with open(f'{filename}', 'w', encoding=ENCODING) as file:
                file.write(file_content)


if __name__ == '__main__':
    main()
