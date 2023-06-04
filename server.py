import cv2
import socket
import pickle
import struct

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set up server host and port
host = 'localhost'  # Replace with your server IP address if needed
port = 8000  # Choose a suitable port number

# Bind the server socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)
print('Server listening on {}:{}'.format(host, port))

# Accept a client connection
client_socket, client_address = server_socket.accept()
print('Connected to client:', client_address)

# Receive the image size from the client
data = b""
payload_size = struct.calcsize("Q")
while len(data) < payload_size:
    data += client_socket.recv(4*1024)
packed_msg_size = data[:payload_size]
data = data[payload_size:]
msg_size = struct.unpack("Q", packed_msg_size)[0]

# Receive the image data from the client
while len(data) < msg_size:
    data += client_socket.recv(4*1024)
frame_data = data[:msg_size]
data = data[msg_size:]

# Deserialize and process the image
frame = pickle.loads(frame_data)
# Apply the desired image processing/filtering using OpenCV
# For example, applying a grayscale filter
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Serialize the processed image
processed_data = pickle.dumps(gray_frame)

# Send the processed image back to the client
client_socket.sendall(struct.pack("Q", len(processed_data)) + processed_data)
