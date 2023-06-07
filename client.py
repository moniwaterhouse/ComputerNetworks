import cv2
import socket
import struct

from common import serialize_img, deserialize_img

class Client:
    def __init__(self, host_addr='localhost', port=8000):
        print('CLIENT: Creating client with Host: {}, Port: {}'.format(host_addr, port))
        self.host = host_addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_host_port(self, host_addr, port):
        self.host = host_addr
        self.port = port

    def connect_to_server(self):
        self.socket.connect((self.host, self.port))
        print('CLIENT: Connected to server {}:{}'.format(self.host, self.port))

    def close_connection(self):
        self.socket.close()

    def read_image_file(self, img_path):
        image_path = img_path
        image = cv2.imread(image_path)
        return image

    def send_data_server(self, serialized_img):
        print('CLIENT: Sending image to server...')
        self.socket.sendall(struct.pack("Q", len(serialized_img)) + serialized_img)

    def receive_processed_img(self):
        print('CLIENT: Receiving processed image from server...')
        # Receive the processed image from the server
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
            data += self.socket.recv(4*1024)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Receive the processed image data from the server
        while len(data) < msg_size:
            data += self.socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        return frame_data

    def display_img(self, deser_img):
        cv2.imshow("Processed Image", deser_img)
        cv2.waitKey(0)

    def save_result_img(self, output_path, deser_img):
        print('CLIENT: saving image to {}'.format(output_path))
        cv2.imwrite(output_path, deser_img)

    def run(self, img_path='puppy1.jpg', output_path='processed_img.jpg'):
        img_obj = self.read_image_file(img_path)
        ser_img = serialize_img(img_obj)
        self.send_data_server(ser_img)
        processed_img = self.receive_processed_img()
        deser_img = deserialize_img(processed_img)
        # self.display_img(deser_img)
        self.save_result_img(output_path, deser_img)
