import pickle
from os import remove
from os.path import exists

def serialize_img(img_obj):
        ser_img = pickle.dumps(img_obj)
        return ser_img

def deserialize_img(frame_data):
        deser_img = pickle.loads(frame_data)
        return deser_img

def clear_files(img_path):
        if exists(img_path):
            remove(img_path)