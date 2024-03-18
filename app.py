from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import psutil
import socket
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

def get_network_info():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    net_io = psutil.net_io_counters()
    return {
        'hostname': hostname,
        'host_ip': host_ip,
        'net_io': {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
    }

def emit_network_info():
    while True:
        network_info = get_network_info()
        socketio.emit('network_info', network_info, namespace='/monitor')
        time.sleep(5)  # Update interval in seconds

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/monitor')
def handle_connect():
    emit_network_info_thread = threading.Thread(target=emit_network_info)
    emit_network_info_thread.daemon = True
    emit_network_info_thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
