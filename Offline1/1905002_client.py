import socket
import pickle
import importlib
import random

aes = importlib.import_module('1905002_aes')
ecc = importlib.import_module('1905002_ecc')

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 12345

client_socket.connect((host, port))

# alice is client
a = -3
b = 4
G = (0, 2)
p = ecc.generate_prime_with_bits(128)

# k_a --> Alice's private key
k_a = p - (1 << 10) * random.randint(1,1000)

# A --> Alice's public key
A = ecc.multiply_point(G, k_a, a, p)

data_to_send =  {'G':G, 'a':a, 'b':b, 'p': p, 'A':A}

# Serialize the dictionary
serialized_data = pickle.dumps(data_to_send)
client_socket.send(serialized_data)

# Receive B from server
data = client_socket.recv(8192)
received_dict = pickle.loads(data)
B = received_dict['B']

(key,y) = ecc.multiply_point(B, k_a, a, p)

# tell that you are ready
client_socket.send(b"I am ready")

# receive a string from the server
msg = client_socket.recv(8192).decode()

if msg == "I am ready":
    print("Enter the message to send: ")
    text = input()
    key = aes.convert_number_key_to_string(key)

    initialization_vector = str(random.randint(10 ** 15, 10 ** 16 - 1)) # 16 digit random number
    encrypted_text = aes.aes_encrypt(text, key, initialization_vector)

    client_socket.send(encrypted_text.encode())

else:
    print("Server not ready. Closing...")
    
client_socket.close()
