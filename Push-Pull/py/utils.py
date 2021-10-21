import socket
import urllib.parse

def get_url(img_path,port):
    #ip = get_host_ip()
    ip = "192.168.191.1"
    #http://192.168.8.65:5111/image/path
    url = "http://"+str(ip)+":"+str(port)+"/image/"+urllib.parse.quote(img_path)
    return url

def get_host_ip(): 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip