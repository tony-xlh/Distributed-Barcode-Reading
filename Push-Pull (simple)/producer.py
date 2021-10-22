import zmq
import os
import urllib.parse
import time

def get_file_url(img_path):
    ip = "192.168.191.1"
    port = 5111
    url = "http://"+str(ip)+":"+str(port)+"/image/"+urllib.parse.quote(img_path)
    return url

def load_files_list(img_folder):
    files_list = []
    for filename in os.listdir(img_folder):
        name, ext = os.path.splitext(filename)
        if ext.lower() in ('.png','.jpg','.jpeg','.bmp','.tif', '.tiff','.pdf'):
            files_list.append(filename)
    return files_list

print("Please input the image folder:")
folder = input()
files_list = load_files_list(folder)
context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.bind("tcp://*:5557")
start_time = int(time.time()*1000)
size = len(files_list)
for filename in files_list:
    url = get_file_url(os.path.join(folder,filename))
    work_message = { 'url': url, 'size': size, 'start_time': start_time}
    print(work_message)
    time.sleep(0.01)
    zmq_socket.send_json(work_message)
