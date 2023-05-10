import os
import socket
from utils import envia_mensagem, recebe_mensagem

def limpaTela():
    """ Limpa a tela. """

    os.system('cls' if os.name == 'nt' else 'clear')


def leCoordenada(dim):
    """ Le um coordenadas de uma peca.
        Retorna uma tupla do tipo (i, j) em caso de sucesso,
        ou False em caso de erro """

    inputDoUsuario = input("Especifique uma peca: ")

    try:
        i = int(inputDoUsuario.split(' ')[0])
        j = int(inputDoUsuario.split(' ')[1])

    except ValueError:
        print("Coordenadas invalidas! Use o formato \"i j\" (sem aspas),")
        print("onde i e j sao inteiros maiores ou iguais a 0 e menores que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    if i < 0 or i >= dim:
        print("Coordenada i deve ser maior ou igual a zero e menor que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    if j < 0 or j >= dim:
        print("Coordenada j deve ser maior ou igual a zero e menor que {0}".format(dim))
        input("Pressione <enter> para continuar...")
        return False

    return f"Coordenadas:{i}:{j}"


def recebeDadosNumericos(msg):
    partes = msg.split(':')
    return int(partes[1])

ip = 'localhost'
port = 10040
addr = (ip, port)
client_socket = socket.socket()
client_socket.connect(addr)
buffer = []

boas_vindas = recebe_mensagem(client_socket).decode()
print(f"{boas_vindas}")

num_sequencial = recebeDadosNumericos(recebe_mensagem(client_socket).decode())
coordenadas= False
print("Aguardando outros jogadores...")
dim = recebeDadosNumericos(recebe_mensagem(client_socket).decode())
print(f"Dimensão do tabuleiro {dim}\n")

while True:
    limpaTela()
    vez = recebeDadosNumericos(recebe_mensagem(client_socket).decode())

    status = recebe_mensagem(client_socket).decode()
    print(f"{status}")

    # Jogada de um jogador
    if num_sequencial == vez:
        # primeira peça
        while True:
            # Vale notar que eu mudei para a checagem se é uma jogada válidar ser
            # feita no cliente ao invés do servidor
            while not coordenadas:
                coordenadas = leCoordenada(dim)
            envia_mensagem(client_socket, coordenadas.encode())
            coordenadas = False
            peca_valida = recebeDadosNumericos(recebe_mensagem(client_socket).decode())
            if peca_valida == 0:
                print("Escolha uma primeira peça ainda fechada!")
                continue
            else:
                break
        status = recebe_mensagem(client_socket).decode()
        print(f"{status}")
        # segunda peça
        while True:
            while not coordenadas:
                coordenadas = leCoordenada(dim)
            envia_mensagem(client_socket, coordenadas.encode())
            coordenadas= False
            peca_valida = recebeDadosNumericos(recebe_mensagem(client_socket).decode())
            if peca_valida == 0:
                print("Escolha uma segunda peçaa ainda fechada!")
                continue
            else:
                break
        status = recebe_mensagem(client_socket).decode()
        print(f"{status}")

    #Mensagens informando as peças escolhidas 
    print(recebe_mensagem(client_socket).decode())
    #Mensagens informando se o jogador da vez pontuou
    print(recebe_mensagem(client_socket).decode())

    fim_de_jogo = recebeDadosNumericos(recebe_mensagem(client_socket).decode())

    if fim_de_jogo != 0:
        break

print(recebe_mensagem(client_socket).decode())


client_socket.close()