# Jogo de Pong em Python
## Descrição do Jogo

_O Pong é um clássico jogo de arcade que simula um jogo de tênis de mesa. O objetivo é acertar a bola com um "paddle" e enviá-la para o campo adversário, evitando que a bola passe pelo próprio "paddle". O jogo continua até que um dos jogadores alcance uma pontuação predeterminada._
Funcionamento do Jogo

## O jogo é dividido em duas partes:
_o cliente e o servidor. O cliente é responsável por exibir a interface do jogo e lidar com a interação do jogador, enquanto o servidor é responsável por coordenar a comunicação entre os clientes e manter o estado do jogo._
## Cliente

_O código do cliente é responsável por criar a interface gráfica do jogo usando a biblioteca Pygame. Ele se conecta ao servidor para permitir que dois jogadores joguem Pong em rede._

_Ao iniciar, o cliente exibe duas opções de conexão: "Conectar digitando IP" e "Conectar automaticamente". O jogador pode escolher uma das opções para se conectar ao servidor. Se selecionar "Conectar digitando IP", ele pode digitar o endereço IP do servidor manualmente. Se selecionar "Conectar automaticamente", o cliente enviará uma mensagem de broadcast para descobrir o endereço IP do servidor._

_Após estabelecer a conexão com o servidor, o cliente exibirá a tela do jogo. Cada jogador controla um "paddle" usando o movimento do mouse. A posição do mouse é enviada ao servidor, que repassa a posição do "paddle" do outro jogador de volta ao cliente. O cliente atualiza a posição do "paddle" e a exibe na tela._

_A bola se move pela tela e rebata nos "paddles" dos jogadores. Se a bola ultrapassar um "paddle" e atingir a borda oposta, o jogador adversário marca um ponto. O jogo continua até que um jogador alcance uma pontuação de 10. Quando isso acontece, o cliente exibe uma mensagem indicando o jogador vencedor e fecha o jogo._
## Servidor

_O código do servidor é responsável por receber as conexões dos clientes e coordenar a comunicação entre eles. Ele utiliza sockets TCP para estabelecer a comunicação._

_O servidor inicia um socket e aguarda a conexão do cliente 1. Após a conexão ser estabelecida, o servidor envia uma mensagem de confirmação ao cliente 1 indicando que ele é o jogador 1. Em seguida, o servidor aguarda a conexão do cliente 2 e envia uma mensagem de confirmação indicando que ele é o jogador 2._

_Durante o jogo, o servidor recebe as teclas pressionadas pelos clientes e as envia de volta para o outro cliente. Isso permite que os "paddles" sejam atualizados em tempo real em ambos os clientes._

_O servidor continua recebendo e enviando as teclas pressionadas até que o jogo seja encerrado._
## Conclusão

O jogo de Pong implementado em Python utilizando os códigos do cliente e servidor fornecidos permite que dois jogadores joguem Pong em rede. Os jogadores podem se conectar ao servidor e controlar seus "paddles" usando o movimento do mouse. O servidor coordena a comunicação entre os jogadores, atualiza o estado do jogo e envia as informações relevantes de volta aos clientes.

## Requisitos

* Python 3 instalado no seu sistema.
* Biblioteca Pygame instalada. Você pode
* instalá-la usando o comando pip install pygame.

## Executando o servidor

* Salve o código do servidor em um arquivo chamado "server.py".

* Abra um terminal ou prompt de comando e navegue até o diretório onde o arquivo "server.py" está localizado.

* Execute o servidor com o comando python server.py.

## Executando o cliente

* Salve o código do cliente em um arquivo chamado "client.py".

* Abra um terminal ou prompt de comando e navegue até o diretório onde o arquivo "client.py" está localizado.

* Execute o cliente com o comando python client.py.

    Siga as instruções exibidas na tela para estabelecer a conexão com o servidor. Você pode escolher conectar digitando o IP manualmente ou permitir que o cliente descubra automaticamente o IP do servidor.

## Jogando o jogo

    Após estabelecer a conexão com o servidor, o jogo será iniciado automaticamente.
    Use o movimento do mouse para controlar o "paddle" no jogo.
    As teclas pressionadas serão transmitidas para o servidor, permitindo a interação entre os jogadores.

__Lembre-se de executar primeiro o servidor e, em seguida, os clientes para que possam se conectar adequadamente. Divirta-se jogando Pong!__