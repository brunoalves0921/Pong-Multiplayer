import socket
import pickle
from threading import Thread
import time
from colorama import Fore, Style

# Configurações da conexão
HOST = "0.0.0.0"
PORT = 3000
BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 3001

# Inicializa o colorama
Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.RESET

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

# Inicializa o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)
print("Servidor iniciado e aguardando conexões...")
IPV4 = socket.gethostbyname(socket.gethostname())
print("[TCP] " + IPV4 + ":" + str(PORT))

thread_broadcast = Thread(target=broadcast, daemon=True)
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

# Variáveis para rastrear o menor e o maior ping e média de ping
min_pings = [float('inf')] * 2
max_pings = [float('-inf')] * 2
total_pings = [[0] * 100, [0] * 100]
contador = 0

# Loop principal do jogo
while True:

    # Recebe as teclas pressionadas pelos clientes

    time1 = time.time()
    data = client1_socket.recv(64)
    client1_keys = pickle.loads(data)

    time2 = time.time()
    data = client2_socket.recv(64)
    client2_keys = pickle.loads(data)
    time3 = time.time()


    # Envia as teclas pressionadas aos clientes

    client1_socket.sendall(pickle.dumps(client2_keys))
    client2_socket.sendall(pickle.dumps(client1_keys))


    pings = [time2 - time1, time3 - time2]

    for i in range(2):
        min_pings[i] = min(min_pings[i], pings[i])
        max_pings[i] = max(max_pings[i], pings[i])
        total_pings[i][contador] = pings[i]


    contador += 1
    if contador == len(total_pings[0]):
        contador = 0

    media_pings = [sum(total_pings[0]) / 100, sum(total_pings[1]) / 100]

    if contador != 60 and contador != 0:
        continue

    for i in range(2):
        # Formata as informações de acordo com o ping
        ping_str = "Ping Player {}: {:.4f} ms".format(i+1, pings[i] * 1000)
        if media_pings[i] <= 0.03: # 30 ms
            ping_str = Fore.GREEN + ping_str + Fore.RESET
        elif media_pings[i] <= 0.05: # 50 ms
            ping_str = Fore.YELLOW + ping_str + Fore.RESET
        else:
            ping_str = Fore.RED + ping_str + Fore.RESET
        # Formata o menor ping
        min_ping_str = "Menor: {:.4f} ms".format(min_pings[i] * 1000)
        min_ping_str = Fore.BLUE + min_ping_str + Fore.RESET

        # Formata o maior ping
        max_ping_str = "Maior: {:.4f} ms".format(max_pings[i] * 1000)
        max_ping_str = Fore.RED + max_ping_str + Fore.RESET

        # Formata o ping médio
        media_ping_str = "Média: {:.4f} ms".format(media_pings[i] * 1000)
        if media_pings[i] <= 0.03: # 30 ms
            media_ping_str = Fore.GREEN + media_ping_str + Fore.RESET
        elif media_pings[i] <= 0.05: # 50 ms
            media_ping_str = Fore.YELLOW + media_ping_str + Fore.RESET
        else:
            media_ping_str = Fore.RED + media_ping_str + Fore.RESET

        # Imprime as informações atualizadas em uma única linha
        print("\r" + ping_str + " | " + min_ping_str + " | " + max_ping_str + " | " + media_ping_str, end=" "*10)

# Fecha as conexões
client1_socket.close()
client2_socket.close()
server_socket.close()
