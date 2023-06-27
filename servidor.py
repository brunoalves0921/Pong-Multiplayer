import socket
import pickle
from threading import Thread

# Configurações da conexão
HOST = "0.0.0.0"
PORT = 3000
BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 3001

def broadcast():
    server_socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #IPV4, UDP (User Datagram Protocol)
    server_socketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Configura o socket para enviar broadcast
    server_socketUDP.bind(("", BROADCAST_PORT)) # Liga o servidor a porta especifica e IP o SO escolhe
    print("[BROADCAST] " + BROADCAST_IP + ":" + str(BROADCAST_PORT))
    while True:
        data, client_address = server_socketUDP.recvfrom(1024) # Espera receber uma mensagem de broadcast, função bloqueante, espera até que uma mensagem seja recebida
        message = data.decode() # Decodifica a mensagem recebida

        if message == "broadcast": # Se a mensagem for broadcast, envia o IP do servidor para o cliente
            IP = socket.gethostbyname(socket.gethostname())
            server_socketUDP.sendto(IP.encode(), client_address)
        print("[BROADCAST]: IP enviado: ", IP + " para o cliente: ", client_address)

    # server_socketUDP.close() # Fecha o socket UDP

# Inicializa o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)
print("Servidor iniciado e aguardando conexões...")
IPV4 = socket.gethostbyname(socket.gethostname())
print("[TCP] " + IPV4 + ":" + str(PORT))

thread_broadcast = Thread(target=broadcast)
thread_broadcast.start()

# Aceita a conexão do cliente 1
client1_socket, client1_address = server_socket.accept()
print("[TCP]: Cliente 1 conectado:", client1_address)

# Envia uma mensagem de confirmação ao cliente 1
client1_socket.sendall(b'connected1')

# Aceita a conexão do cliente 2
client2_socket, client2_address = server_socket.accept()
print("[TCP]: Cliente 2 conectado:", client2_address)

# Envia uma mensagem de confirmação ao cliente 2
client2_socket.sendall(b'connected2')

# Loop principal do jogo
while True:
    # Recebe as teclas pressionadas pelos clientes
    data = client1_socket.recv(1024)
    client1_keys = pickle.loads(data)

    data = client2_socket.recv(1024)
    client2_keys = pickle.loads(data)

    # Envia as teclas pressionadas aos clientes
    client1_socket.sendall(pickle.dumps(client2_keys))
    client2_socket.sendall(pickle.dumps(client1_keys))

# Fecha as conexões
client1_socket.close()
client2_socket.close()
server_socket.close()
