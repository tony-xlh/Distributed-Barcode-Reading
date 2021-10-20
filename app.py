#coding=utf-8
from flask import Flask, request, render_template, send_file
from batch_session import Batch_session
import os
import zmq
import threading
import time


def result_collector():
    print("result collector")
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
        update_session_processed(result)

def update_session_processed(result):
    session_id=result["session_id"]
    session = get_session(session_id)
    session.processed = session.processed + 1
    print(session.get_process())
    if session.completed():
        elapsed_time = int((time.time() - session.start_time) * 1000)
        elapsed_times[session_id] = elapsed_time
        print("Session completed in " + str(elapsed_time) + "ms.")

app = Flask(__name__, static_url_path='/', static_folder='static')

sessions={}
elapsed_times={}
port=5111

threading.Thread(target=result_collector, args=()).start()

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/session/create/<folderpath>')
def create_session(folderpath):
    print(folderpath)
    session = Batch_session(folderpath)
    session_id = session.id
    sessions[session_id]=session
    return {"status":"success","session_id":session_id}
    
@app.route('/session/<session_id>/start/')
def start_session(session_id):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    session.start_reading()
    return "Started"


def get_session(session_id):
    session = None
    if session_id in sessions:
        session = sessions[session_id]
    return session
    
@app.route('/session/<session_id>/progress/')
def get_session_progress(session_id):
    session = get_session(session_id)
    if session == None:
        return "Not exist"
    return session.get_process()
    
@app.route('/session/<session_id>/time/')
def get_session_time(session_id):
    if session_id in elapsed_times:
        return str(elapsed_times[session_id])
    else:
        return str(0)

@app.route('/image/<img_path>')
def get_image(img_path):
    print(img_path)
    return send_file(img_path)

if __name__ == '__main__':
    #create_and_start_session("test")
    app.run(host='0.0.0.0',port=port)
    
