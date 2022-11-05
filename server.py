#!usr/bin/env python3  

"""
This is a socket server capable of handling multiple clients at once. With three channels for notes : python, software testing, and database.
There are three commands that can be used to interact with the server: Read (R), Write (W), and Quit (Q).
The server will send a message to the client when it is connected and when it is disconnected.
"""

__author__ = 'Anton Maynard CS 3280'
__version__ = 'Fall 2022'
__pylint__ = 'v1.8.3'


import socket
import sys
import threading
import time

# Global variables
HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

# Global dictionary to store the notes
notes = {'python': '', 'software testing': '', 'database': ''}
# Global dictionary to store the clients
clients = {}

# Global lock
lock = threading.Lock()

# Global variable to store the number of clients
num_clients = 0


def main():
    """
    This function will create a socket, bind it to the host and port, and listen for connections.
    """
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the host and port
        s.bind((HOST, PORT))
        # Listen for connections
        s.listen()
        # Print a message to the server
        print('Server is running...')
        # Accept connections
        while True:
            # Accept a connection
            conn, addr = s.accept()
            # Create a new thread for the client
            threading.Thread(target=client_thread, args=(conn, addr)).start()


def client_thread(conn, addr):
    """
    This function will handle the client thread.
    """
    # Global variables
    global num_clients
    global command
    global channel

    # Lock the thread
    lock.acquire()
    # Increment the number of clients
    num_clients += 1
    # Unlock the thread
    lock.release()

    # Print a message to the server
    print(f'Client {num_clients} connected from {addr[0]}:{addr[1]}')

    
    # Receive the channel from the client
    conn.sendall('Please enter a channel: python(PY), software testing(QA), or database(DB).'.encode(ENCODING))
    channel = conn.recv(BUFFER_SIZE).decode(ENCODING).lower()
    
     # Receive read, write, or quit from the client
    command = get_command(conn)
    
    # Add the client to the dictionary
    clients[num_clients] = conn
    
    # Loop until the client quits
    while command != 'q' and command != 'quit':
        # If the client wants to read the notes
        if command == 'R':
            # Send the notes to the client
            send_notes(conn,channel)
            get_command(conn)
        # If the client wants to write to the notes
        elif command == 'W':
            # Ask the client for the size of note 
            conn.sendall('Please enter the size of the data: '.encode(ENCODING))
            size = int(conn.recv(BUFFER_SIZE).decode(ENCODING))
            
            # Ask the client to send note
            conn.sendall('Send the note'.encode(ENCODING))
            note = conn.recv(BUFFER_SIZE).decode(ENCODING)
            
            # Add the note to the notes dictionary
            notes[channel] += note
            
            command = get_command(conn)

    # Lock the thread
    lock.acquire()
    # Decrement the number of clients
    num_clients -= 1
    # Unlock the thread
    lock.release()

    # Print a message to the server
    print(f'Client {num_clients} disconnected from {addr[0]}:{addr[1]}')

    # Close the connection
    conn.close()


def get_command(connection) -> str:
    """
    This function will get the command from the client.
    """
    # Receive the command from the client
    connection.sendall('Please enter a channel: python(PY), software testing(QA), or database(DB).'.encode(ENCODING))
    command = connection.recv(BUFFER_SIZE).decode(ENCODING).lower()

    # Return the channel
    return command

def write_notes(conn, channel):
    """
    This function will write the notes to the client.
    """
    # Global variables
    global notes

    # Write the notes to the client

    if channel == 'python':
        notes['python'] = conn.recv(BUFFER_SIZE).decode(ENCODING)
    elif channel == 'software testing':
        notes['software testing'] = conn.recv(BUFFER_SIZE).decode(ENCODING)
    elif channel == 'database':
        notes['database'] = conn.recv(BUFFER_SIZE).decode(ENCODING)

 ##HERE

def send_notes(conn, channel):
    """
    This function will send the notes to the client.
    """
    # Global variables
    global notes

    # Send the notes to the client

    if channel == 'python':
        conn.sendall(notes['python'].encode(ENCODING))
    elif channel == 'software testing':
        conn.sendall(notes['software testing'].encode(ENCODING))
    elif channel == 'database':
        conn.sendall(notes['database'].encode(ENCODING))


if __name__ == '__main__':
    main()