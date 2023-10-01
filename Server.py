import socket, sys, pygame, threading, json
import time
from typing import Any

from settings import *
from player import Player
from ping import FPSCounter

class Server:
    def __init__(self):

        self.new_clients = []
        self.clients = {}


        self.udp_server = UDPServer(self.new_clients, self.clients)
        self.udp_server.start()

        self.tcp_server = TCPServer()
        self.tcp_server.start()

        
    
    def send(self, message, protocol):
        if protocol == 'UDP':
            self.udp_server.data_to_send = message
        elif protocol == 'TCP':
            self.tcp_server.send_to_all_clients(message)
    

    def receive(self, protocol):
        if protocol == 'UDP':
            return self.udp_server.clients
        elif protocol == 'TCP':
            return self.tcp_server.data_received
        else:
            return None


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


class Client:
    def __init__(self):
        self.id = None
        self.tcp_adress = None
        self.udp_adress = None


        self.player = Player()
    
    def update_player(self, data):
        self.player.inputs = data['inputs']
    

    

        
class TCPServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.server_socket.bind((HOST, TCP_PORT))
                break
            except OSError:
                time.sleep(1)

        self.server_socket.listen(5)  # Permet jusqu'à 5 connexions simultanées
        self.client_connections = []  # Liste pour stocker les connexions des clients
    
        self.data_received = {}


    def run(self):
        print(f"Serveur TCP en écoute sur {HOST}:{TCP_PORT} ...")
        while True:
            client_socket, adress = self.server_socket.accept()
            print("Nouvelle connexion établie :", adress)
            self.client_connections.append(client_socket)  # Ajouter la connexion du client

    # def handle_client(self, client_socket):
    #     while True:
    #         data = client_socket.recv(1024)
    #         if not data:
    #             break
    #         message = data.decode('utf-8')
    #         print(f"Reçu du client : {message}")
    #         # Traitez le message du client ici
    #         # Réponse au client si nécessaire

    # def accept_connections(self):
    #     print("Serveur en écoute...")
    #     while True:
    #         client_socket, _ = self.server_socket.accept()
    #         print("Nouvelle connexion établie.")
    #         self.client_connections.append(client_socket)  # Ajouter la connexion du client


            # client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            # client_handler.start()

    def send_to_all_clients(self, message):
        for client_socket in self.client_connections:
            try:
                message
                client_socket.send(json.dumps(message).encode('utf-8'))
            except:
                print("Erreur de transmission")
                # Gérer les erreurs de communication avec un client
                pass
    
    def close(self):
        self.server_socket.close()


class Main:
    def __init__(self):
        
        # server
        self.server = Server()

        # display
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('SERVER')

        self.players = []

        # ping
        self.fps_counter = FPSCounter('MAIN')

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting")
                self.udp_server.close()
                pygame.quit()
                sys.exit()
        
        return_key = self.test_tcp()
        if return_key:
            self.server.send("Tree Burn", 'TCP')
        
    def test_tcp(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            return True
        
        return False
            
    def draw(self):

        self.update_players()
        for player in self.players:
            player.move(player.inputs)

            pygame.draw.rect(self.display_surface, player.color, (player.get_position()[0], player.get_position()[1], 40, 40))


    def update_players(self):
        clients = self.server.receive('UDP')
        self.players = []
        message = {}
        for adress, client in clients.items():
            self.players.append(client.player)
            message[str(adress)] = {'pos' : client.player.get_position(), 'color' : client.player.color}
        
        self.server.send(message, 'UDP')

        
    
    def run(self):
        # event
        self.event_loop()

        # drawing
        self.display_surface.fill('beige')
        self.draw()

        # update
        self.fps_counter.ping()
        pygame.display.update()


if __name__ == "__main__":
    main = Main()
    while True:
        main.run()
        