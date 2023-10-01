
import uuid
from player import Player


class Client:
    def __init__(self):
        self.id = str(uuid.uuid4()).split('-')[0]
        self.tcp_adress = None
        self.udp_adress = None


        self.player = Player()
    
    def update_player(self, data):
        self.player.inputs = data['inputs']
    