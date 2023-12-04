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

def get_keys():
    p = ecc.generate_prime_with_bits(128)
    (a,b,G) = ecc.generate_parameters(p)

    # k_a --> Alice's private key
    k_a = random.randint(1<<127, p-1)

    # A --> Alice's public key
    A = ecc.multiply_point(G, k_a, a, p)

    return (p,a,b,G,k_a,A)

def establish_shared_key():
    (p,a,b,G,k_a,A) = get_keys()
    data_to_send =  {'G':G, 'a':a, 'b':b, 'p': p, 'A':A}

    # Serialize the dictionary
    serialized_data = pickle.dumps(data_to_send)
    client_socket.send(serialized_data)

    # Receive B from server
    data = client_socket.recv(8192)
    received_dict = pickle.loads(data)
    B = received_dict['B']

    (key,y) = ecc.multiply_point(B, k_a, a, p)

    return aes.convert_number_key_to_string(key)

def send_message(text, key):

    initialization_vector = str(random.randint(10 ** 15, 10 ** 16 - 1)) # 16 digit random number
    encrypted_text = aes.aes_encrypt(text, key, initialization_vector)

    client_socket.send(encrypted_text.encode())
    return True

key = establish_shared_key()

    # tell that you are ready
client_socket.send(b"I am ready")

    # receive a string from the server
msg = client_socket.recv(8192).decode()

if msg != "I am ready":
    print("Server not ready. Closing...")
    client_socket.close()
    exit()


while True:

    print("Enter a message to send:(Q to close) ", end="")
    text = input()

    if text == "Q" or text == "q" or text == "":
        send_message("close connection", key)
        break

    else:
        send_message(text, key)
        print("Message sent")

    key = establish_shared_key()
    
client_socket.close()
