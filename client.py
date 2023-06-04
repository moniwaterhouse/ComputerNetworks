import cv2
import socket
import pickle
import struct

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set up server host and port
host = 'localhost'  # Replace with your server IP address if needed
port = 8000  # Choose the same port number used by the server

# Connect to the server
client_socket.connect((host, port))
print('Connected to server:', (host, port))

# Read the image file
image_path = 'puppy.jpg'  # Replace with the path to your image
image = cv2.imread(image_path)

# Serialize the image
data = pickle.dumps(image)

# Send the image size to the server
client_socket.sendall(struct.pack("Q", len(data)) + data)

# Receive the processed image from the server
data = b""
payload_size = struct.calcsize("Q")
while len(data) < payload_size:
    data += client_socket.recv(4*1024)
packed_msg_size = data[:payload_size]
data = data[payload_size:]
msg_size = struct.unpack("Q", packed_msg_size)[0]

# Receive the processed image data from the server
while len(data) < msg_size:
    data += client_socket.recv(4*1024)
frame_data = data[:msg_size]
data = data[msg_size:]

# Deserialize the processed image
processed_image = pickle.loads(frame_data)

# Display the processed image
cv2.imshow("Processed Image", processed_image)
cv2.waitKey(0)

# Save the processed image
output_path = 'new_image.jpg'  # Replace with the desired output path and file name
cv2.imwrite(output_path, processed_image)

