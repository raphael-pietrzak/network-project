import json, socket, sys, threading, time, pygame
from Network.Client.client import Client
from ping import FPSCounter
from settings import *
        


class Main:
    def __init__(self):

        self.fps_counter = FPSCounter('MAIN')

        pygame.init()
        self.client = Client()
        self.players = {}

        
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('CLIENT')


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                self.client.close()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('[ EVENT ] : Return pressed')
                    self.client.send('Client Pressed Return', 'TCP')
                    if not self.client.is_online():
                        self.client.start()
                        


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
        self.update_players()
        for pid, player in self.players.items():
            pygame.draw.rect(self.display_surface, player['color'], (player['pos'][0], player['pos'][1], 40, 40))


    def update_players(self):
        players = self.client.receive('UDP')
        self.players = players
        
        # for adress, player in players.items():
        #     if adress in self.players:
        #         self.players[adress]['pos'] = player['pos']
        #         self.players[adress]['color'] = player['color']
        #     else:
        #         self.players[adress] = player


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



