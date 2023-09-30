import socket, sys, pygame, threading, json

from settings import *
from player import Player
from ping import FPSCounter


class UDPServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.data_to_send = {}
        self.data_received = {}
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clients = {}
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
        data = json.dumps(message).encode('utf-8')
        self.udp_socket.sendto(data, client_address)

    def handle_udp_message(self, client_address, data):
        try :
            message = json.loads(data.decode('utf-8'))
            player = self.clients.get(client_address)
            if not player:
                player = Player()
                self.clients[client_address] = player

            player.inputs = message['inputs']

            response = {str(adress) : {'pos' : player.get_position(), 'color' : player.color} for adress, player in self.clients.items()}

            self.send_udp_message(client_address, response)
            

        except json.JSONDecodeError:
            print('JSONDecodeError')
            return
        
        except KeyError:
            print('KeyError')
            return
    

        
class TCPServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, TCP_PORT))
        self.server_socket.listen(5)  # Permet jusqu'à 5 connexions simultanées
        self.client_connections = []  # Liste pour stocker les connexions des clients
    
    def run(self):
        print(f"Serveur TCP en écoute sur {HOST}:{TCP_PORT}...")
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
                client_socket.send(message.encode('utf-8'))
            except:
                print("Erreur de transmission")
                # Gérer les erreurs de communication avec un client
                pass
    
    def close(self):
        self.server_socket.close()


class Main:
    def __init__(self):
        self.udp_server = UDPServer()
        self.udp_server.start()

        self.tcp_server = TCPServer()
        self.tcp_server.start()


        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('SERVER')

        self.fps_counter = FPSCounter('MAIN')

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting")
                self.udp_server.close()
                pygame.quit()
                sys.exit()
        
        if self.TCPTest():
            self.tcp_server.send_to_all_clients(self.TCPTest())
        
    def TCPTest(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            return "Tree Burn"
        
        return None
            
    def draw(self):
        self.fps_counter.ping()
        for adress, player in self.udp_server.clients.items():
            player.move(player.inputs)
            pygame.draw.rect(self.display_surface, player.color, (player.get_position()[0], player.get_position()[1], 40, 40))
    
    def run(self):
        self.event_loop()
        self.display_surface.fill('beige')
        self.draw()
        pygame.display.update()


if __name__ == "__main__":
    main = Main()
    while True:
        try:
            main.run()
        except KeyboardInterrupt as e:
            print("[EVENT] : Keyboard interrupt")
            main.udp_server.close()
            main.tcp_server.close()
            pygame.quit()
            sys.exit()