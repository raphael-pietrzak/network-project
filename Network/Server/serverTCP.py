import json
import socket
import threading
import time

from settings import *


class TCPServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.server_socket.bind((HOST, TCP_PORT))
                break
            except OSError:
                time.sleep(1)

        self.server_socket.listen(5)  # Permet jusqu'à 5 connexions simultanées
        self.client_connections = []  # Liste pour stocker les connexions des clients
    
        self.data_received = {}


    def run(self):
        print(f"Serveur TCP en écoute sur {HOST}:{TCP_PORT} ...")
        while True:
            client_socket, adress = self.server_socket.accept()
            print("Nouvelle connexion établie :", adress)
            self.client_connections.append(client_socket)  # Ajouter la connexion du client

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, adress,))
            client_handler.start()

    def handle_client(self, client_socket, adress):
        self.data_received[adress] = []
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            message = self.handle_client_message(data)
            print(f"Reçu du client {adress} : {message}")
            if message:
                self.data_received[adress].append(message)

            # Traitez le message du client ici
            # Réponse au client si nécessaire

    
    def handle_client_message(self, message):
        try:
            message = json.loads(message)
            return message

        except json.JSONDecodeError:
            print('Erreur de lecture du message')
            return None


    def send_to_all_clients(self, message):
        for client_socket in self.client_connections:
            try:
                message
                client_socket.send(json.dumps(message).encode('utf-8'))
            except:
                print("Erreur de transmission")
                # Gérer les erreurs de communication avec un client
                pass
    
    def close(self):
        self.server_socket.close()
