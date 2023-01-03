import pickle
import socket
import datetime
import threading
import time

class ServerThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.sock.accept()
            try:
                print('connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    time.sleep(0.01 )
                    # Get the current date and time
                    current_datetime = datetime.datetime.now()

                    # Pickle the date and time object
                    pickled_datetime = pickle.dumps(current_datetime)
                    #print(f'Message length is: {len(pickled_datetime)}')

                    # Send the pickled data to the client
                    connection.sendall(pickled_datetime)
            finally:
                # Clean up the connection
                connection.close()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Create a new thread to handle the incoming connection
server_thread = ServerThread(sock)
server_thread.start()
