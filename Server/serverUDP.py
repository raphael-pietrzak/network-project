import json, socket, threading
from ping import FPSCounter
from settings import *



class UDPServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.is_running = True

        self.client_data = {}
        self.server_data = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((HOST, UDP_PORT))
        print(f"Serveur UDP en écoute sur {HOST}:{UDP_PORT} ...")

        self.network_fps_counter = FPSCounter('SERVER UDP')



    def run(self):
        while self.is_running:
            try:
                data, addr = self.server_socket.recvfrom(BUFFER_SIZE)
                data = json.loads(data.decode(ENCODING)) 
                if not data: continue

                uuid = data['uuid']
                message = data['message']
                self.client_data[uuid] = message


                self.server_socket.sendto(json.dumps(self.server_data).encode(ENCODING), addr)

                self.network_fps_counter.ping()

            except Exception as e:
                print(f'Error UDP server send/receive : {e}')
                continue
    

    def close(self):
        self.is_running = False
        self.server_socket.close()
