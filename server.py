import io
import socket
from PIL import Image, ImageFilter

# Server configuration variables
HOST_IP = 'localhost'
PORT = 5000

# This function applies the filter to the image that has been received by the client
def apply_filter(image):
    new_image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return new_image

# Receives the image data from the client
def receive_data(client):
    client_data = b''
    while True:
        chunk = client.recv(2048)
        client_data += chunk
        if len(chunk) < 2048:
            break
        

    # Creates a pillow image from the received image data in form of bytes
    image = Image.open(io.BytesIO(client_data))


    new_image = apply_filter(image)

    # Converts the new image to bytes to send it to the client again
    new_image_data = io.BytesIO()
    new_image.save(new_image_data, format='JPEG')
    new_image_bytes = new_image_data.getvalue()

    # Send the new image back to the client
    client.sendall(new_image_bytes)

    # Close the client socket
    client.close()

def run():
    # Creates a server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binds the server socket to the host and port
    server.bind((HOST_IP, PORT))

    # Listens for incoming connections
    server.listen()

    print("The server is listening on IP: ", HOST_IP)

    while True:
        # Accepts a client connection
        client_socket, client_address = server.accept()
        print("Accepted connection from", client_address[0])

        # Handle the client connection
        receive_data(client_socket)

if __name__ == '__main__':
    run()
