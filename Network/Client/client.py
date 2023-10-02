from Network.Client.clientTCP import TCPClient
from Network.Client.clientUDP import UDPClient


class Client:
    def __init__(self):

        self.udp_client = UDPClient()
        self.udp_client.start()

        self.tcp_client = TCPClient()
        self.tcp_client.start()


    def send(self, message, protocol):
        match protocol:
            case 'TCP': self.tcp_client.send(message)
            case 'UDP': self.udp_client.client_data = message
            case _: return None
    
    
    def receive(self, protocol):
        match protocol:
            case 'TCP': return self.tcp_client.server_data
            case 'UDP': return self.udp_client.server_data
            case _: return None


    def is_online(self):
        return self.tcp_client.is_running and self.udp_client.is_running

    
    def close(self):
        self.udp_client.close()
        self.tcp_client.close()
    