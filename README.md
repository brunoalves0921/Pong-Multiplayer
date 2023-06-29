# Pong Multiplayer

Este projeto consiste em um jogo de Pong multiplayer simples em que dois jogadores podem pressionar teclas e enviar comandos um ao outro. O jogo é baseado em um servidor centralizado que gerencia as interações entre os jogadores.

## Funcionamento

O servidor é iniciado e aguarda a conexão de dois clientes. Quando os clientes se conectam, eles podem pressionar teclas para controlar seus personagens no jogo. Esses comandos são enviados ao servidor, que os encaminha para o jogador oposto. Isso permite que os jogadores interajam em tempo real.

## Dependências

O projeto requer as seguintes dependências:

- Python 3.x
- Biblioteca `socket`
- Biblioteca `pickle`
- Biblioteca `threading`
- Biblioteca `time`
- Biblioteca `colorama`

Certifique-se de ter essas dependências instaladas em seu ambiente antes de executar o projeto.

## Executando o Projeto

Para executar o projeto, siga as etapas abaixo:

1. Certifique-se de ter o Python instalado em seu sistema.
2. Execute o arquivo `server.py` para iniciar o servidor.
3. Execute para cada jogador o arquivo `client.py`, depois disso os jogadores podem se conectar usando o endereço IP exibido pelo servidor ou fazer uma conexão automática selecionando a opção correspondente.
4. Uma vez conectados, os jogadores podem pressionar as teclas para controlar suas raquetes no jogo.
5. O servidor gerenciará o envio dos comandos para o jogador oposto, permitindo a interação multiplayer.

## Contribuições

Contribuições são bem-vindas! Se você deseja contribuir com este projeto, siga as etapas abaixo:

1. Faça um fork deste repositório.
2. Crie uma branch para suas alterações: `git checkout -b minha-branch`.
3. Faça as alterações desejadas e faça commit delas: `git commit -m "Minha contribuição"`.
4. Envie as alterações para o seu repositório fork: `git push origin minha-branch`.
5. Abra um pull request neste repositório.

## Autor

Jorge Bruno Costa Alves. Universidade Federal do Ceará - Campus Quixadá.
