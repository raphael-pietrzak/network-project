
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
        self.client_socket.settimeout(3.0)



    def run(self):
        while True:
            self.client_socket.sendto(json.dumps(self.data_to_send).encode('utf-8'), (SERVER_IP, UDP_PORT))
            response, addr = self.client_socket.recvfrom(1024)
            self.data_received = json.loads(response.decode('utf-8'))

            # print(f"Reçu du serveur ({addr}): {self.data_received}")


class TUDPClient(threading.Thread):
    def __init__(self):
        super().__init__()
        self.data_to_send = {}
        self.data_received = {}

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(3.0)  # Définir un timeout d'1 seconde
        self.is_running = True


        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.daemon = True  # Permet de terminer le thread de réception lorsque le programme principal se termine

        self.sending_fps_counter = FPSCounter('SENDING')
        self.receive_fps_counter = FPSCounter('RECEIVING')


    def start(self):
        super().start()
        self.receive_thread.start()


    def run(self):
        while self.is_running:
            self.sending_fps_counter.ping()


            message = self.data_to_send
            if not message:
                print('None message')
                time.sleep(0.1)
                continue
            
            try:
                data = json.dumps(message).encode('utf-8')
                self.udp_socket.sendto(data, (SERVER_IP, UDP_PORT))

                time.sleep(0.001) #  0.0001 max

            except:
                print('Erreur Envoi UDP')
            
                
            

            


    def receive(self):
        while self.is_running:
            self.receive_fps_counter.ping()
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                self.handle_udp_message(addr, data)
            except :
                print('Erreur Recv UDP')

    
    def handle_udp_message(self, addr, data):
        try :
            self.data_received = json.loads(data.decode('utf-8'))
        except:
            print('Erreur : buffer too small')


    def close(self):
        self.is_running = False
        self.udp_socket.close()