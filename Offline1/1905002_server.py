import socket
import pickle
import importlib
import random

aes = importlib.import_module('1905002_aes')
ecc = importlib.import_module('1905002_ecc')
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = '127.0.0.1'
port = 12345
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {host}:{port}")

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

# Receive data from the client
data = client_socket.recv(8192)

# Deserialize the received data using pickle
received_dict = pickle.loads(data)
print(received_dict)

a = received_dict['a']
b = received_dict['b']
p = received_dict['p']
G = received_dict['G']
A = received_dict['A']

k_b = p - (1 << 10) * random.randint(1,1000)
B = ecc.multiply_point(G, k_b, a, p)
data_to_send = {'B':B}
serialized_data = pickle.dumps(data_to_send)
client_socket.send(serialized_data)

R = ecc.multiply_point(A, k_b, a, p)
print("R =", R)

# receive a string from the client
data = client_socket.recv(8192)
msg = data.decode()
print(msg)
if msg == "Hello server! I am Alice.":    
        # send a string that says "Hello client! I am Bob."
        client_socket.send(b"Hello client! I am Bob.")
        # receive a string from the client
        # encrypted_data = client_socket.recv(8192)
        # # decrypt the data using AES
        # data = aes.decrypt(encrypted_data)
# print(data.decode())




print("Received dictionary:", received_dict)

# Close the sockets
client_socket.close()
server_socket.close()
