import zmq
import random
import requests
from BarcodeReader import DynamsoftBarcodeReader


ip = "127.0.0.1"
consumer_id = random.randrange(1,10005) #Create an ID for the consumer
print("I am consumer #"+str(consumer_id))
context = zmq.Context()
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.connect("tcp://"+ip+":5557")
consumer_sender = context.socket(zmq.PUSH)
consumer_sender.connect("tcp://"+ip+":5558")
reader = DynamsoftBarcodeReader()
while True:
    work = consumer_receiver.recv_json()
    url = work['url']
    reading_result=reader.decode_file_stream(requests.get(url).content) # The requests library is used to download images
    result = { 'consumer' : consumer_id, 'reading_result' : reading_result, 'url': url, 'size': work['size'], 'start_time': work['start_time']}
    #print(result)
    consumer_sender.send_json(result)