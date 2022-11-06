## Client-side for the server.py program

# Import the socket module
import socket
HOST = '127.0.0.1'
PORT = 50003
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
        
        # Get the inital message from the server
        message = sock.recv(BUFFER_SIZE).decode()
        channel = input(message)
        
        # Send the channel to the server
        sock.sendall(channel.encode(ENCODING))
        
        while sock.recv(BUFFER_SIZE).decode(ENCODING) != 'exit':
            # Get the message from the server
            message = sock.recv(BUFFER_SIZE).decode()
            # Print the message
            command = input(message)
            # Send the message to the server
            sock.sendall(command.encode(ENCODING))


if __name__ == '__main__':
    main()