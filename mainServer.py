from player import Player
from settings import *

import sys, pygame

from Server.server import Server
from ping import FPSCounter





class Main:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('SERVER')

        # server
        self.server = Server()
        self.players = {}

        # groups
        self.player_sprites = pygame.sprite.Group()

        # ping
        self.fps_counter = FPSCounter('MAIN')

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ EVENT ] : Window closed")
                self.server.close()
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('[ EVENT ] : Return pressed')
                    self.server.send('Server Pressed Return', 'TCP')

            
    def update_players(self):
        new_players = self.server.get_new_clients()
        for uuid in new_players:
            player = Player(self.player_sprites)
            self.players[uuid] = player
            

        del_players = self.server.get_del_clients()
        for uuid in del_players:
            self.player_sprites.remove(player)
            del self.players[uuid]

        clients_data = self.server.receive('UDP')
        for uuid, data in clients_data.items():
            player = self.players.get(uuid)
            if not player: break
            player.inputs = data['inputs']
        
        message = {uuid: {'color': player.color, 'pos': player.get_position()} for uuid, player in self.players.items()}
        self.server.send(message, 'UDP')


        
    
    def run(self):
        # event
        self.event_loop()

        # drawing
        self.display_surface.fill('beige')
        self.update_players()
        for player in self.player_sprites:
            player.move()
            player.draw()

        # update
        self.fps_counter.ping()
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    main = Main()
    while True:
        main.run()
        