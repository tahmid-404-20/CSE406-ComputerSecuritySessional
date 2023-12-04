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

def establish_shared_key():
        # receive dictionary
        data = client_socket.recv(8192)
        # data is a dictionary, so deserialize it
        received_dict = pickle.loads(data)
        # print(received_dict)

        a = received_dict['a']
        b = received_dict['b']
        p = received_dict['p']
        G = received_dict['G']
        A = received_dict['A']

        # bob is server
        
        # k_b --> Bob's private key
        k_b = random.randint(1<<127, p-1)
        # B --> Bob's public key
        B = ecc.multiply_point(G, k_b, a, p)

        data_to_send = {'B':B}
        serialized_data = pickle.dumps(data_to_send)
        client_socket.send(serialized_data)

        (key, y) = ecc.multiply_point(A, k_b, a, p)

        return aes.convert_number_key_to_string(key)        

key = establish_shared_key()

# receive a string from the client
msg = client_socket.recv(8192).decode()

if msg == "I am ready":    
        client_socket.send(b"I am ready")

        while True:
                # receive encrypted text
                encrypted_text = client_socket.recv(8192).decode()

                # print(key.encode('ascii', 'replace'))
                decrypted_text = aes.aes_decrypt(encrypted_text, key)
                print("Decrypted text:", decrypted_text)

                if decrypted_text == "close connection":
                        break

                key = establish_shared_key()
else:
        print("Client not ready. Closing...")

# Close the sockets
client_socket.close()
server_socket.close()
