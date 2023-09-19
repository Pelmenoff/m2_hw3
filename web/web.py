import socket
import os
import json
import threading
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, abort

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'message': request.form.get('message')
        }
        file_path = 'web/storage/data.json'
        save_message(data, file_path)
        return render_template('message.html', data=data)
    return render_template('message.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def ensure_storage_directory():
    storage_dir = 'web/storage'
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)

    file_path = os.path.join(storage_dir, 'data.json')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)

def udp_server():
    ensure_storage_directory()

    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = server_socket.recvfrom(1024)
        data_dict = json.loads(data.decode())
        save_message(data_dict)

def udp_client(username, message_text):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    data_dict = {
        "username": username,
        "message": message_text
    }

    data_str = json.dumps(data_dict)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(data_str.encode(), (UDP_IP, UDP_PORT))
    client_socket.close()

def save_message(data_dict, file_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[timestamp] = data_dict

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    udp_thread = threading.Thread(target=udp_server)
    udp_thread.start()

    app.run(port=3000)