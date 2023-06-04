import socket

# Server configuration variables
SERVER_IP = '192.168.0.100'
SERVER_PORT = 5000

def send_image(image_path):
    # Reads the image file
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # CreateS a TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ConnectS to the server
    client.connect((SERVER_IP, SERVER_PORT))
    print("Connected to server at IP: ", SERVER_IP)

    # SendS the image data to the server
    client.sendall(image_data)

    # ReceiveS the filtered image from the server
    filtered_image_data = b''
    while True:
        chunk = client.recv(2048)
        filtered_image_data += chunk
        if len(chunk) < 2048:
            break
        

    # SaveS the filtered image
    with open('new_image.jpg', 'wb') as f:
        f.write(filtered_image_data)

    print("Filter added to the image successfully")

    # Close the client socket
    client.close()

if __name__ == '__main__':
    image_path = 'puppy2.jpg' 
    send_image(image_path)
