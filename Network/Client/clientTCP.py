
import json
import socket
import threading

from settings import *


class TCPClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_received = {}
        self.is_running = True
    
    def start(self):

        self.client_socket.connect((HOST, TCP_PORT))
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()


    def receive_messages(self):
        while self.is_running:
            try:
                data = self.client_socket.recv(1024)
            except OSError:
                continue
            if not data:
                break
            message = data.decode('utf-8')
            self.data_received = json.loads(message)
    
    def send(self, message):
        data = json.dumps(message)
        self.client_socket.send(data.encode('utf-8'))
    
    def close(self):
        self.is_running = False
        self.client_socket.close()