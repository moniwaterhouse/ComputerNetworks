import cv2
import socket
import pickle
import struct

from common import serialize_img, deserialize_img

class Server():
    def __init__(self, host_addr='localhost', port=8000):
        print('SERVER: Creating server with Host: {}, Port: {}'.format(host_addr, port))
        self.host = host_addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

        self.client_socket = None
        self.client_addr = None

    def set_host_port(self, host_addr, port):
        self.host = host_addr
        self.port = port

    def listen_for_connections(self):
        print('SERVER: Server listening on {}:{}...'.format(self.host, self.port))
        self.socket.listen(5)

    def accept_connection(self):
        self.client_socket, self.client_addr = self.socket.accept()
        print('SERVER: Connected to client:', self.client_addr)

    def connect_client(self):
        self.listen_for_connections()
        self.accept_connection()

    def close_connection(self):
        if self.client_socket != None:
            self.client_socket.close()

    def receive_incoming_img(self):
        print('SERVER: Receiving image to process...')
        # Receive the image size from the client
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
            data += self.client_socket.recv(4*1024)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Receive the image data from the client
        while len(data) < msg_size:
            data += self.client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        return frame_data

    def apply_grayscale_filter(self, deser_img):
        filtered_img = cv2.cvtColor(deser_img, cv2.COLOR_BGR2GRAY)
        return filtered_img

    def send_data_client(self, ser_img):
        self.client_socket.sendall(struct.pack("Q", len(ser_img)) + ser_img)

    def run(self):
        self.connect_client()
        ser_img = self.receive_incoming_img()
        deser_img = deserialize_img(ser_img)
        filtered_img = self.apply_grayscale_filter(deser_img)
        ser_filtered_img = serialize_img(filtered_img)
        self.send_data_client(ser_filtered_img)
