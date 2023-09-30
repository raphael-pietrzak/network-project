import json, socket, sys, threading, time, pygame
from ping import FPSCounter
from settings import *
        


class UDPClient(threading.Thread):
    def __init__(self):
        super().__init__()
        self.data_to_send = {}
        self.data_received = {}
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
            time.sleep(0.0001)


    def receive(self):
        while self.is_running:
            self.receive_fps_counter.ping()
            data, addr = self.udp_socket.recvfrom(1024)
            self.handle_udp_message(addr, data)

    
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
        self.client_socket.connect((HOST, TCP_PORT))
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Client: Reçu - {message}")
    
    def close(self):
        self.client_socket.close()

class Main:
    def __init__(self):
        pygame.init()
        self.udp_client = UDPClient()
        self.udp_client.start()

        self.tcp_client = TCPClient()


        self.fps_counter = FPSCounter('MAIN')

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('CLIENT')

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[EVENT] : Window closed")
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

    def run(self):
        self.event_loop()
        self.display_surface.fill('aliceblue')
        self.udp_client.data_to_send = {'inputs': self.get_keyboard_inputs()}
        self.draw()
        pygame.display.update()
    
    def draw(self):
        players = self.udp_client.data_received

        self.fps_counter.ping()
        for player in players.values():
            pygame.draw.rect(self.display_surface, player['color'], (player['pos'][0], player['pos'][1], 40, 40))



if __name__ == "__main__":
    main = Main()
    while True:
        try:
            main.run()
        except KeyboardInterrupt as e:
            print("[EVENT] : Keyboard interrupt")
            main.udp_client.close()
            main.tcp_client.close()
            pygame.quit()
            sys.exit()



