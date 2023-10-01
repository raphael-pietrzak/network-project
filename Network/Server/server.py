from Network.Server.serverTCP import TCPServer
from Network.Server.serverUDP import UDPServer


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
