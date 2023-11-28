import socket
import pickle
import importlib
import random

aes = importlib.import_module('1905002_aes')
ecc = importlib.import_module('1905002_ecc')

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
host = '127.0.0.1'
port = 12345

# Connect to the server
client_socket.connect((host, port))

# alice is client
a = -3
b = 4
G = (0, 2)
p = ecc.generate_prime_with_digits(16)

k_a = p - (1 << 10) * random.randint(1,1000)

A = ecc.multiply_point(G, k_a, a, p)

data_to_send =  {'G':G, 'a':a, 'b':b, 'p': p, 'A':A}

# Serialize the dictionary using pickle
serialized_data = pickle.dumps(data_to_send)

# Send the serialized data to the server
client_socket.send(serialized_data)

# Receive data from the server
data = client_socket.recv(8192)
received_dict = pickle.loads(data)

B = received_dict['B']

R = ecc.multiply_point(B, k_a, a, p)

print("R =", R)

# send a string that says "Hello server! I am Alice."
client_socket.send(b"Hello server! I am Alice.")

# receive a string from the server
data = client_socket.recv(8192)
msg = data.decode()
print(msg)

# Close the socket
client_socket.close()
