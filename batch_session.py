#coding=utf-8
import json
import os
import time
import threading
import uuid
import zmq
import utils

class Batch_session():
    def __init__(self, img_folder, port=5111, session_id=None):
        self.img_folder = img_folder
        self.id = uuid.uuid1().hex
        if session_id != None:
            self.id = session_id
        self.files_list = []
        self.processed = 0
        self.load_files_list()
        self.start_time = 0
        self.port = port

    def start_reading(self):
        self.processed = 0
        self.start_time = time.time()
        threading.Thread(target=self.dispatch, args=()).start()
            
    def load_files_list(self):
        for filename in os.listdir(self.img_folder):
            name, ext = os.path.splitext(filename)
            if ext.lower() in ('.png','.jpg','.jpeg','.bmp','.tif', '.tiff','.pdf'):
                self.files_list.append(filename)

    def dispatch(self):
        print("dispatch")
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://127.0.0.1:5557")
        # Start your result manager and workers before you start your producers
        for filename in self.files_list:
            work_message = { 'session_id' : self.id, 'url': self.get_file_url(filename) }
            time.sleep(0.01)
            zmq_socket.send_json(work_message)
            
    def get_file_url(self, filename):
        return utils.get_url(os.path.join(self.img_folder,filename),self.port)

    def completed(self):
        if len(self.files_list) == self.processed:
            return True
        else:
            return False

    def get_process(self):
        return "{}/{}".format(self.processed, len(self.files_list))


if __name__ == '__main__':
    session = Batch_session("./test","./tmp")
    session.start_reading()
    while session.completed()==False:
        time.sleep(0.2)
        print(session.get_process())
    print("Completed")
    
        