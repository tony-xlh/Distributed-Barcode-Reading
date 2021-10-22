import time
import zmq
context = zmq.Context()
results_receiver = context.socket(zmq.PULL)
results_receiver.bind("tcp://*:5558")
collecter_data = {}
decoded = 0
while True:
    result = results_receiver.recv_json()
    decoded = decoded + 1
    if result['consumer'] in collecter_data:
        collecter_data[result['consumer']] = collecter_data[result['consumer']] + 1
    else:
        collecter_data[result['consumer']] = 1
    print(collecter_data)
    if result['size']==decoded:
        elapsedTime = int(time.time())*1000 - result['start_time']
        print("Done in "+str(elapsedTime))
        decoded=0
        collecter_data = {}