## Client-side for the server.py program

# Import the socket module
import socket
HOST = '127.0.0.1'
PORT = 54121
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
            server_Message = sock.recv(BUFFER_SIZE).decode()
            # Display the message from the server to the client
            if server_Message == 'exit':
                connected = False
                socket.close()
            elif server_Message == 'Channel':
                handle_channel(sock)
            elif server_Message == 'What':
                handle_what(sock)
            elif server_Message == 'Write':
                handle_write(sock)
            elif server_Message == 'Read':
                handle_read(sock)

            
            

def handle_channel(sock):
    """
    This function will handle the channel message.
    """
    client_message = input('Please enter a channel: python(PY), software testing(QA), or database(DB).')
    sock.sendall(client_message.encode(ENCODING))
    
def handle_what(sock):
    client_message = input('Would you like to Write(W), Read(R) or Quit(Q)?')
    sock.sendall(client_message.encode(ENCODING))
    
    
def handle_write(sock):
    """
    This function will handle the write message.
    """
    client_message = input('Please enter the size of the data: ')
    sock.sendall(client_message.encode(ENCODING))
    
def handle_read(sock):
    """
    This function will handle the read message.
    """
    notes = sock.recv(BUFFER_SIZE).decode(ENCODING)
    ## Write notes to a file
    
    

if __name__ == '__main__':
    main()