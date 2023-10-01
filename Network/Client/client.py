from Network.Client.clientTCP import TCPClient
from Network.Client.clientUDP import UDPClient


class Client:
    def __init__(self):
        self.udp_client = UDPClient()
        self.udp_client.start()
        self.online = True


        # try:
        #     self.tcp_client = TCPClient()
        #     self.tcp_client.start()

        # except ConnectionError:
        #     print('Impossible de se connecter au serveur')
        #     self.close()
        #     self.online = False




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