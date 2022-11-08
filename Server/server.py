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
import logging as logger
import os
from datetime import datetime

# Global variables
HOST = '127.0.0.1'
PORT = 54121
BUFFER_SIZE = 1024
ENCODING = 'utf-8'


# Global dictionary to store the notes
#notes = {'python': [], 'software testing': [], 'database': []}
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Bind the socket to the host and port
        sock.bind((HOST, PORT))
        # Listen for connections
        sock.listen()
        # Print a message to the server
        print('Server is running...')
        # Accept connections
        while True:
            # Accept a connection
            connection, address = sock.accept()
            # Create a new thread for the client
            ClientThread(connection, address).start()
            print(f'Client connected at {address}')

##TODO MAKE COMMAND A GLOBAL VARIABLE
class ClientThread(threading.Thread):
    """
    This class will create a thread for each client.
    """
    num_clients = 0
    command = ''
    connection = None
    address = None
    channel = ''
    def __init__(self, connection, address):
        """
        This function will initialize the thread.
        """
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.client_thread()
    
    def client_thread(self):
        """
        This function will handle the client thread.
        """

        # Lock the thread
        lock.acquire()
        # Increment the number of clients
        self.num_clients += 1
        # Unlock the thread
        lock.release()

        # Log a message to the server
        print(f'Client {self.num_clients} connected from {self.address[0]}:{self.address[1]}')
        
        # Receive the channel from the client
        self.connection.sendall('Channel'.encode(ENCODING))
        self.channel = self.connection.recv(BUFFER_SIZE).decode(ENCODING).lower()
        
        # Receive read, write, or quit from the client
        self.get_command()
        
        # Add the client to the dictionary
        clients[self.num_clients] = self.connection
        
        connected = True
        # Loop until the client quits
        while connected:
            # If the client wants to read the notes
            if self.command == 'r' or self.command == 'read':
                # Send the notes to the client
                self.connection.sendall('Read'.encode(ENCODING))
                self.send_notes()
            # If the client wants to write to the notes
            elif self.command == 'w' or self.command == 'write':
                self.connection.sendall('Size'.encode(ENCODING))
                self.write_notes()
            elif self.command == 'q' or self.command == 'quit':
                connected = False
            else:
                # Ask the client to enter a valid command
                self.connection.sendall('Invalid What'.encode(ENCODING))
                self.command = self.connection.recv(BUFFER_SIZE).decode(ENCODING).lower()

        # Send exit message to client
        self.connection.sendall('exit'.encode(ENCODING))
        # Lock the thread
        lock.acquire()
        # Decrement the number of clients
        self.num_clients -= 1
        # Unlock the thread
        lock.release()

        # Print a message to the server
        print(f'Client {num_clients} disconnected from {self.address[0]}:{self.address[1]}')
        
        # Close the connection
        self.connection.close()

    def get_command(self):
        """
        This function will get the command from the client.
        """
        # Receive the command from the client
        self.connection.sendall('What'.encode(ENCODING))
        self.command = self.connection.recv(BUFFER_SIZE).decode(ENCODING).lower()


    def write_notes(self):
        """
        This function will write the notes to the client.
        """
        
        # Write the notes to the client
        if self.channel == 'python' or self.channel == 'py':
            self.write_note_to_file('python')
        elif self.channel == 'software testing' or self.channel == 'qa':
            self.write_note_to_file('software testing')
        elif self.channel == 'database' or self.channel == 'db':
            self.write_note_to_file('database')
            
        self.get_command()
    
    def write_note_to_file(self,directory):
        """
        This function will write the notes to the client.
        """
        size = self.get_size()
        note = self.connection.recv(size).decode(ENCODING)
        # Writes note to the file in the passed in directory
        with open(f'{directory}//{self.address[0]}__{datetime.now()}.txt', 'w', encoding= ENCODING) as file:
            file.write(note)
        
    def send_notes(self):
        """
        This function will send the notes to the client.
        """

        if self.channel == 'python' or self.channel == 'py':
            self.read_all_notes_in_channel('python')
        elif self.channel == 'software testing' or self.channel == 'qa':
            self.read_all_notes_in_channel('software testing')
        elif self.channel == 'database' or self.channel == 'db':
            self.read_all_notes_in_channel('database')

        self.get_command()

    def read_all_notes_in_channel(self,directory):
        """
        This function will read all the notes from a specific directory.
        """
        # Read all the notes from the file
        print('Reading notes...')
        notes = ''
        for file in os.listdir(f'{directory}'):
            with open(f'{directory}/{file}', 'r', encoding= ENCODING) as file:
                note_content = file.read()
                notes += f'{file.name}<BOF>{note_content}<EOF>'

        print('Notes read.')
        self.connection.sendall(f'{notes} <EOT>'.encode(ENCODING))
        reception = self.connection.recv(BUFFER_SIZE).decode(ENCODING)
        if reception == 'Received':
            print('Notes sent.')
        else:
            print('Error sending notes.')
        
    def get_size(self) -> int:
        """
        This function will get the size of the note from the client.
        """
        valid = False
        
        # Get size from client
        self.connection.sendall('Please enter the size of the data: '.encode(ENCODING))
        size = self.connection.recv(BUFFER_SIZE).decode(ENCODING)
        
        # Loop until the size is valid
        while not valid:
            try:
                size = int(size)
                if size > 0 & size < 1024:
                    valid = True
                elif size > 1024:
                    self.connection.sendall('Please enter a number within range 0-1024: '.encode(ENCODING))
                    size = self.connection.recv(BUFFER_SIZE).decode(ENCODING)
            except ValueError:
                self.connection.sendall('Please enter a number within range 0-1024 for the size.')
                size = self.connection.recv(BUFFER_SIZE).decode(ENCODING)
        return size


if __name__ == '__main__':
    main()