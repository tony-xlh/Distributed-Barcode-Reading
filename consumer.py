import time
import zmq
import random
import requests
from BarcodeReader import DynamsoftBarcodeReader

def consumer():
    reader = DynamsoftBarcodeReader()
    consumer_id = random.randrange(1,10005)
    print("I am consumer #%s" % (consumer_id))
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:5557")
    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://127.0.0.1:5558")
    
    while True:
        work = consumer_receiver.recv_json()
        url = work['url']
        #reading_result=reader.decode_file(url)
        reading_result=reader.decode_file_stream(requests.get(url).content)
        result = { 'consumer' : consumer_id, 'reading_result' : reading_result, 'session_id': work['session_id']}
        consumer_sender.send_json(result)

consumer()