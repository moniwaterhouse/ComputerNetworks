from client import Client
from common import clear_files

INPUT_IMG = 'puppy1.jpg'
OUTPUT_PATH = 'result_1.jpg'

clear_files(OUTPUT_PATH)
client = Client()
client.connect_to_server()
client.run(img_path=INPUT_IMG, output_path=OUTPUT_PATH)
client.socket.close()