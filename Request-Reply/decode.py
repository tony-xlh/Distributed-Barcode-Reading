import zmq

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6666")
while True:
    print("Input image path: ")
    img_path = input()
    socket.send(bytes(img_path,"utf-8"))
    message = socket.recv()
    print(message.decode("utf-8"))