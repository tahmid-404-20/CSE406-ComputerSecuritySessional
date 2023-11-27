import socket
import pickle

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
host = '127.0.0.1'
port = 12345

# Connect to the server
client_socket.connect((host, port))

# Create a sample dictionary
data_to_send = {'key1': 'value1', 'key2': 'value2', 'key3': 42}

# Serialize the dictionary using pickle
serialized_data = pickle.dumps(data_to_send)

# Send the serialized data to the server
client_socket.send(serialized_data)

# Close the socket
client_socket.close()
