import socket
import pickle
import pygame
from pygame.locals import *
from sys import exit

# Configurações da tela
WIDTH, HEIGHT = 640, 360  # Reduzido
WHITE = (255, 255, 255)
FPS = 60

# Classe para o jogador/paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 40))  # Menor
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        # Limita o movimento dentro da tela
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Classe para a bola
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 8))  # Menor
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_x = 6  # Um pouco mais lento também
        self.speed_y = 6

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Verifica colisões com as bordas da tela
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Variáveis de controle do jogo
isPlayer1 = None
IP = ''
score_player1 = 0
score_player2 = 0
font = pygame.font.Font(None, 28)  # Fonte menor

# Carrega o som da colisão da bola com a raquete
collision_sound = pygame.mixer.Sound('collision_sound.mp3')

def broadcast():
    BROADCAST_IP = "255.255.255.255"
    BROADCAST_PORT = 3001
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind(("", 0))
    client_socket.sendto(b"broadcast", (BROADCAST_IP, BROADCAST_PORT))
    data, server_address = client_socket.recvfrom(1024)
    IP = data.decode()
    client_socket.close()
    return IP

# inicia a tela principal do jogo com opções de conexão
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    screen.fill((0, 0, 0))

    # botões
    connect_button = pygame.draw.rect(screen, WHITE, (40, HEIGHT // 2 - 40, 240, 80))
    connect_text = font.render("Conectar digitando IP", True, (0, 0, 0))
    screen.blit(connect_text, (40 + (240 - connect_text.get_width()) // 2, HEIGHT // 2 - connect_text.get_height() // 2))

    connect_button2 = pygame.draw.rect(screen, WHITE, (360, HEIGHT // 2 - 40, 240, 80))
    connect_text2 = font.render("Conectar automático", True, (0, 0, 0))
    screen.blit(connect_text2, (360 + (240 - connect_text2.get_width()) // 2, HEIGHT // 2 - connect_text2.get_height() // 2))

    pygame.display.flip()

    if pygame.mouse.get_pressed()[0]:
        if connect_button.collidepoint(pygame.mouse.get_pos()):
            score_text = font.render(f"Conectando ao servidor...", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
            pygame.display.flip()
            ok = False
            while not ok:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            ok = True
                            try:
                                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                client_socket.connect((IP, 3000))
                            except:
                                screen.fill((0, 0, 0))
                                score_text = font.render(f"Erro ao conectar ao servidor, tente novamente!", True, WHITE)
                                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
                                pygame.display.flip()
                                pygame.time.delay(3000)
                                ok = False
                        elif event.key == K_BACKSPACE:
                            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                                IP = ''
                            else:
                                IP = IP[:-1]
                        else:
                            IP += event.unicode
                screen.fill((0, 0, 0))
                score_text = font.render(f"Conectando ao servidor...", True, WHITE)
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
                ip_text = font.render(f"IP: {IP}", True, WHITE)
                screen.blit(ip_text, (WIDTH // 2 - ip_text.get_width() // 2, HEIGHT // 2 - ip_text.get_height() // 2))
                pygame.display.flip()
            break

        elif connect_button2.collidepoint(pygame.mouse.get_pos()):
            score_text = font.render(f"Conectando ao servidor...", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
            pygame.display.flip()
            IP = broadcast()
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((IP, 3000))
                ok = True
            except:
                screen.fill((0, 0, 0))
                score_text = font.render(f"Erro ao conectar ao servidor, tente novamente!", True, WHITE)
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
                pygame.display.flip()
                pygame.time.delay(3000)
                ok = False
            break

# Recebe a mensagem do servidor
data = client_socket.recv(1024)
if data == b'connected1':
    pygame.display.set_caption("Pong - Jogador 1")
    screen.fill((0, 0, 0))
    score_text = font.render(f"Conexão estabelecida com o servidor. Você é o jogador 1.", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
    pygame.display.flip()
    isPlayer1 = True
if data == b'connected2':
    pygame.display.set_caption("Pong - Jogador 2")

# Cria a bola
ball = Ball(WIDTH // 2, HEIGHT // 2)

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    data = pickle.dumps(pygame.mouse.get_pos()[1])
    client_socket.sendall(data)

    data = client_socket.recv(1024)
    server_paddle_y = pickle.loads(data)

    screen.fill((0, 0, 0))
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)

    if isPlayer1:
        paddle1 = Paddle(10, pygame.mouse.get_pos()[1])
        paddle2 = Paddle(WIDTH - 10, server_paddle_y)
    else:
        paddle1 = Paddle(10, server_paddle_y)
        paddle2 = Paddle(WIDTH - 10, pygame.mouse.get_pos()[1])

    paddle_group = pygame.sprite.Group(paddle1, paddle2)
    paddle_group.update()
    paddle_group.draw(screen)

    ball.update()
    screen.blit(ball.image, ball.rect)

    if pygame.sprite.spritecollide(ball, paddle_group, False):
        ball.speed_x *= -1
        collision_sound.play()

    if ball.rect.left < 0:
        score_player2 += 1
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed_x *= -1
    elif ball.rect.right > WIDTH:
        score_player1 += 1
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed_x *= -1

    if score_player1 == 10 or score_player2 == 10:
        player_vencedor = 1 if score_player1 == 10 else 2
        score_text = font.render(f"Player {player_vencedor} ganhou!", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        exit()

    score_text = font.render(f"Player 1: {score_player1}  Player 2: {score_player2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(FPS)
