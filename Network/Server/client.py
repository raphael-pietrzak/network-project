
import time
import uuid
from player import Player


class Client:
    def __init__(self):
        self.id = str(uuid.uuid4()).split('-')[0]
        self.player = Player()
        self.last_udp_timestamp = time.time()
    
    def update_player(self, data, protocol):
        if protocol == 'TCP':
            pass
        if protocol == 'UDP':
            self.player.inputs = data['inputs']
            self.last_udp_timestamp = time.time()
    
    def check_timout(self):
        if time.time() - self.last_udp_timestamp > 3:
            return True
        return False