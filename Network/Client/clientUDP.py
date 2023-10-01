
import json
import socket
import threading
import time

from ping import FPSCounter
from settings import *



class UDPClient(threading.Thread):
    def __init__(self, ):

        super().__init__()
        self.data_received = {}
        self.data_to_send = {}
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(1.0)

        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.receive_thread.start()


        self.network_fps_counter = FPSCounter('NETWORK')



    def run(self):
        while True:
            try:
                self.network_fps_counter.ping()


                
                # SEND

                self.client_socket.sendto(json.dumps(self.data_to_send).encode('utf-8'), (SERVER_IP, UDP_PORT))

                # #DEBUG
                # print(f"Sent to server: {self.data_to_send}")


                # RECEIVE

                # response, addr = self.client_socket.recvfrom(1024)
                # self.data_received = json.loads(response.decode('utf-8'))

                # #DEBUG
                # print(f"Received from server: {self.data_received}")


            except TimeoutError:
                print('Timeout')
                pass

    def receive(self):
        while True:
            try:
                response, addr = self.client_socket.recvfrom(1024)
                self.data_received = json.loads(response.decode('utf-8'))
            except:
                pass
