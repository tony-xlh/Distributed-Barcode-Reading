import zmq
context = zmq.Context()
results_receiver = context.socket(zmq.PULL)
results_receiver.bind("tcp://*:5558")
collecter_data = {}
while True:
    result = results_receiver.recv_json()
    if result['consumer'] in collecter_data:
        collecter_data[result['consumer']] = collecter_data[result['consumer']] + 1
    else:
        collecter_data[result['consumer']] = 1
    print(collecter_data)