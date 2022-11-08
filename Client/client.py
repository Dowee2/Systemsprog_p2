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
            test = sock.recv(BUFFER_SIZE)
            print(test)
            print(test.decode(ENCODING))
            server_Message = test.decode(ENCODING)
            # Display the message from the server to the client
            if server_Message == 'exit':
                connected = False
            elif server_Message == 'Channel':
                handle_channel(sock)
            elif server_Message == 'What':
                handle_what(sock)
            elif server_Message == 'Write':
                handle_write(sock)
            elif server_Message == 'Read':
                handle_read(sock)
            elif server_Message == 'Invalid What':
                handle_invalid_what(sock)

            
            

def handle_channel(sock):
    """
    This function will handle the channel message.
    """
    client_message = input('Please enter a channel: python(PY), software testing(QA), or database(DB).')
    sock.sendall(client_message.encode(ENCODING))
    
def handle_what(sock):
    """
    This function will handle the what message.
    """
    client_message = input('Would you like to Write(W), Read(R) or Quit(Q)?\n')
    sock.sendall(client_message.encode(ENCODING))

def handle_invalid_what(sock):
    """
    This function will handle the invalid what message.
    """
    client_message = input('Please enter a valid command: R, W, or Q \n')
    sock.sendall(client_message.encode(ENCODING))
    
def handle_write(sock):
    """
    This function will handle the write message.
    """
    client_message = input('Please enter the size of the data: ')
    sock.sendall(client_message.encode(ENCODING))
    
def handle_read(sock):
    """
    Writes the recieved notes to a file and spceifies the file location. Also prints the notes to the console
    """
    notes = ''
    while True:
        stream = sock.recv(BUFFER_SIZE).decode(ENCODING)
        notes += stream
        if stream.endswith('<EOT>'):
            sock.sendall('Received'.encode(ENCODING))
            notes.replace('<EOT>','')
            break
    notes = notes.split('<EOF>')

    for note in notes:
        file_name, file_content = note.split('<BOF>')
        print(file_content)
        filename = file_name.split('/')[1]
        with open(f'{filename}', 'w', encoding= ENCODING) as file:
            file.write(file_content)

if __name__ == '__main__':
    main()