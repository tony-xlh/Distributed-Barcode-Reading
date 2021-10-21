import time
import zmq
import random
import requests
import sys
from BarcodeReader import DynamsoftBarcodeReader

def consumer(ip):
    reader = DynamsoftBarcodeReader()
    consumer_id = random.randrange(1,10005)
    print("I am consumer #%s" % (consumer_id))
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://"+ip+":5557")
    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://"+ip+":5558")
    
    while True:
        work = consumer_receiver.recv_json()
        url = work['url']
        #reading_result=reader.decode_file(url)
        reading_result=reader.decode_file_stream(requests.get(url).content)
        result = { 'consumer' : consumer_id, 'reading_result' : reading_result, 'session_id': work['session_id'], 'url': url}
        print(result)
        consumer_sender.send_json(result)


if __name__=="__main__":
    ip="127.0.0.1"
    if len(sys.argv)==2:
        ip=sys.argv[1]
    print("Using ip: "+ip)
    consumer(ip)
    