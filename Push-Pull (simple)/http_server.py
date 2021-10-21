#coding=utf-8
from flask import Flask, send_file

app = Flask(__name__, static_url_path='/', static_folder='static')
port = 5111

@app.route('/image/<img_path>')
def get_image(img_path):
    print(img_path)
    return send_file(img_path)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port)