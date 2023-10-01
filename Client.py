import json, socket, sys, threading, time, pygame
from ping import FPSCounter
from settings import *
        


class Client:
    def __init__(self):
        self.udp_client = UDPClient()
        self.udp_client.start()


        try:
            self.tcp_client = TCPClient()
            self.tcp_client.start()

        except ConnectionError:
            print('Impossible de se connecter au serveur')
            self.close()




    def send(self, message, protocol):
        if protocol == 'UDP':
            self.udp_client.data_to_send = message
        elif protocol == 'TCP':
            self.tcp_client.send(message)
    
    def receive(self, protocol):
        if protocol == 'UDP':
            return self.udp_client.data_received
        elif protocol == 'TCP':
            return self.tcp_client.data_received
        else:
            return None
    
    def close(self):
        self.udp_client.close()
        self.tcp_client.close()


class UDPClient(threading.Thread):
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
            message = self.data_to_send
            try:
                data = json.dumps(message).encode('utf-8')
            except json.JSONDecodeError:
                print('Erreur de lecture du message')
            

            if data == b'{}':
                continue

            self.sending_fps_counter.ping()

            self.udp_socket.sendto(data, (SERVER_IP, UDP_PORT))
            time.sleep(0.001) #  0.0001 max


    def receive(self):
        while self.is_running:
            self.receive_fps_counter.ping()
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                self.handle_udp_message(addr, data)
            except socket.timeout:
                pass
            except OSError:
                continue

    
    def handle_udp_message(self, addr, data):
        try :
            self.data_received = json.loads(data.decode('utf-8'))
            
        except json.JSONDecodeError:
            print('Erreur de lecture du message')
            return

    def close(self):
        self.is_running = False
        self.udp_socket.close()



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

class Main:
    def __init__(self):

        self.fps_counter = FPSCounter('MAIN')

        pygame.init()
        self.client = Client()
        
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('CLIENT')


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                self.client.close()
                pygame.quit()
                sys.exit()


    def get_keyboard_inputs(self):
        keys = pygame.key.get_pressed()

        self.inputs = []

        if keys[pygame.K_LEFT]:
            self.inputs.append("left")
        if keys[pygame.K_RIGHT]:
            self.inputs.append("right")
        if keys[pygame.K_UP]:
            self.inputs.append("up")
        if keys[pygame.K_DOWN]:
            self.inputs.append("down")
        
        return self.inputs

    
    def draw(self):
        players = self.client.receive('UDP')

        self.fps_counter.ping()
        for player in players.values():
            pygame.draw.rect(self.display_surface, player['color'], (player['pos'][0], player['pos'][1], 40, 40))

    def run(self):
        # Ping

        self.event_loop()
        self.display_surface.fill('aliceblue')
        message = {'inputs': self.get_keyboard_inputs()}
        self.client.send(message, 'UDP')
        self.draw()

        self.fps_counter.ping()

        pygame.display.update()


if __name__ == "__main__":
    main = Main()
    while True:
        main.run()



