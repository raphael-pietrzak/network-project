import json
import socket
import threading
from Network.Server.client import Client
from ping import FPSCounter
from settings import *


class UDPServer(threading.Thread):
    def __init__(self, new_clients, clients):
        super().__init__()
        self.new_clients = new_clients
        self.clients = clients
        self.data_to_send = {}
        self.data_received = {}
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.is_running = True


        self.fps_counter = FPSCounter('UDP SERVER')
        

    def run(self):
        self.udp_socket.bind((HOST, UDP_PORT))
        print(f"Serveur UDP en écoute sur {HOST}:{UDP_PORT}...")

        while self.is_running:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                self.fps_counter.ping()
                self.handle_udp_message(addr, data)
            except Exception as e:
                print(e)
                continue    

    def close(self):
        self.is_running = False
        self.udp_socket.close()

        

    def send_udp_message(self, client_address, message):
        try:
            data = json.dumps(message).encode('utf-8')
            self.udp_socket.sendto(data, client_address)
        except json.JSONDecodeError:
            print('JSONDecodeError')

    def handle_udp_message(self, client_address, data):
        try :
            message = json.loads(data.decode('utf-8'))
            client = self.clients.get(client_address)
            if not client:
                client = Client()
                self.clients[client_address] = client

            client.update_player(message)

            self.send_udp_message(client_address, self.data_to_send)
            

        except json.JSONDecodeError:
            print('JSONDecodeError')
            return
        
        except KeyError:
            print('KeyError')
            return
