import os
import socket
from utils import envia_mensagem, recebe_mensagem


def limpaTela():
    """Limpa a tela."""

    os.system("cls" if os.name == "nt" else "clear")


def leCoordenada(dim, jogada):
    """Le as coordenadas de uma peca.
    Retorna uma tupla do tipo (i, j) em caso de sucesso,
    ou False em caso de erro"""

    # jogada = 0 se for a primeira, jogada = 1 se for a segunda
    if jogada:
        inputDoUsuario = input("Escolha a segunda peça: ").strip()
    else:
        inputDoUsuario = input("Escolha a primeira peça: ").strip()

    try:
        i = int(inputDoUsuario.split(" ")[0])
        j = int(inputDoUsuario.split(" ")[1])

    except ValueError:
        print('\nCoordenadas inválidas! Use o formato "i j" (sem aspas), ', end="")
        print("onde i e j são inteiros maiores ou iguais a 0 e menores que {0}.\n".format(dim))
        return False

    if i < 0 or i >= dim:
        print("\nCoordenada i deve ser maior ou igual a zero e menor que {0}\n".format(dim))
        return False

    if j < 0 or j >= dim:
        print("\nCoordenada j deve ser maior ou igual a zero e menor que {0}\n".format(dim))
        return False

    return f"Coordenadas:{i}:{j}"


def recebeDadosNumericos(msg):
    """Extrai os dados de mensagens recebidas."""
    partes = msg.split(":")
    return int(partes[1])


# ip = "localhost", port = 10040
ip = input("\nInsira o endereço de IP do servidor: ")
port = int(input("\nInsira o número da porta: "))
addr = (ip, port)

client_socket = socket.socket()
client_socket.connect(addr)
buffer = []

boas_vindas = recebe_mensagem(client_socket).decode()
print(f"{boas_vindas}")

num_sequencial = recebeDadosNumericos(recebe_mensagem(client_socket).decode())
coordenadas = False

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

        # Primeira peça
        while True:
            while not coordenadas:
                coordenadas = leCoordenada(dim, 0)

            envia_mensagem(client_socket, coordenadas.encode())

            coordenadas = False

            peca_valida = recebeDadosNumericos(recebe_mensagem(client_socket).decode())

            if peca_valida == 0:
                print("\nEscolha uma primeira peça ainda fechada!")
                continue

            else:
                limpaTela()
                break

        status = recebe_mensagem(client_socket).decode()
        print(f"{status}")

        # Segunda peça
        while True:
            while not coordenadas:
                coordenadas = leCoordenada(dim, 1)

            envia_mensagem(client_socket, coordenadas.encode())
            coordenadas = False

            peca_valida = recebeDadosNumericos(recebe_mensagem(client_socket).decode())

            if peca_valida == 0:
                print("\nEscolha uma segunda peça ainda fechada!")
                continue

            else:
                limpaTela()
                break

        status = recebe_mensagem(client_socket).decode()
        print(f"{status}")

    # Mensagens informando as peças escolhidas
    print(recebe_mensagem(client_socket).decode())

    # Mensagens informando se o jogador da vez pontuou
    print(recebe_mensagem(client_socket).decode())

    fim_de_jogo = recebeDadosNumericos(recebe_mensagem(client_socket).decode())

    if fim_de_jogo != 0:
        break

print(recebe_mensagem(client_socket).decode())

client_socket.close()
