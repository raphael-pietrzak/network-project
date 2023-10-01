from settings import *

import sys, pygame

from Network.Server.server import Server
from ping import FPSCounter





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
            self.server.send("Server Pressed Return", 'TCP')
        
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
            message[client.id] = {'pos' : client.player.get_position(), 'color' : client.player.color}
        
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
        