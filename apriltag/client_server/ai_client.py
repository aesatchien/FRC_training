import pickle
import socket
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

finished = False
count = 0
try:
    # Receive the data in small chunks and retransmit it
    while not finished:
        # Receive the pickled date and time object
        count = count + 1
        pickled_datetime = sock.recv(53)

        # Unpickle the date and time object
        current_datetime = pickle.loads(pickled_datetime)

        # Print the date and time
        if count % 100 == 0:
            print(current_datetime)

except KeyboardInterrupt:
    finished = True
finally:
    # Clean up the connection
    sock.close()
