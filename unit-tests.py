import threading
from os import remove
from os.path import exists
from unittest import TestCase, main

from server import Server
from client import Client
from common import clear_files

class TestSuite(TestCase):
    def test_01_client_server_connection_success(self):
        print("\n*** Starting test case 01 ***")
        # Expected results
        EXP_CLIENT_ADDR = '127.0.0.1'

        server = Server(host_addr='localhost', port=8000)
        client = Client(host_addr='localhost', port=8000)

        server_thread = threading.Thread(target=self.start_server, args=(server,))
        server_thread.start()
        client.connect_to_server()
        client.close_connection()
        server_thread.join()

        self.assertEqual(server.client_addr[0], EXP_CLIENT_ADDR, "Error")
        self.clear_sockets(server, client)
        print("### SUCCESS ###")

    def test_02_image_transmission_processing_success(self):
        print("\n*** Starting test case 02 ***")
        # Input Data
        IMG_PATH = 'puppy1.jpg'
        OUTPUT_PATH = 'processed_image.jpg'

        # Expected Results
        IMG_EXISTS = True

        # Initial Conditions
        clear_files(OUTPUT_PATH)
        server = Server(host_addr='localhost', port=8000)
        client = Client(host_addr='localhost', port=8000)

        server_thread = threading.Thread(target=server.run)
        server_thread.start()
        self.run_client(client, img_path=IMG_PATH, output_path=OUTPUT_PATH)
        server_thread.join()
        
        img_exists = exists(OUTPUT_PATH)
        self.assertEqual(IMG_EXISTS, img_exists)
        self.clear_sockets(server, client)
        print("### SUCCESS ###")

    def start_server(self, server):
        server.listen_for_connections()
        server.accept_connection()
        handler_thread = threading.Thread(target=server.close_connection)
        handler_thread.start()

    def run_client(self, client, img_path, output_path):
        client.connect_to_server()
        client.run(img_path, output_path)

    def clear_sockets(self, server, client):
        client.close_connection()
        server.close_connection()
        server.socket.close()

if __name__ == '__main__':
    main()