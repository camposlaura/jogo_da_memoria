import os
import socket
import sys
import time
import random

from JogoDaMemoria import MeuSoquete


def limpaTela():
    """ Limpa a tela. """

    os.system('cls' if os.name == 'nt' else 'clear')

def fechaPeca(tabuleiro, i, j):
    """ Fecha peca na posicao (i, j).
        Se posicao ja esta fechada ou se ja foi removida, retorna False.
        Caso contrario, retorna True. """

    if tabuleiro[i][j] == '-':
        return False

    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False
def novoTabuleiro(dim):
    """ Cria um novo tabuleiro com pecas aleatorias.
        'dim' eh a dimensao do tabuleiro, necessariamente par. """

    # Cria um tabuleiro vazio.
    tabuleiro = []
    for i in range(0, dim):

        linha = []
        for j in range(0, dim):
            linha.append(0)

        tabuleiro.append(linha)

    # Cria uma lista de todas as posicoes do tabuleiro.
    # Util para sortearmos posicoes aleatoriamente para as pecas.
    posicoesDisponiveis = []
    for i in range(0, dim):

        for j in range(0, dim):
            posicoesDisponiveis.append((i, j))

    # Varre todas as pecas que serao colocadas no tabuleiro e posiciona
    # cada par de pecas iguais em posicoes aleatorias.
    for j in range(0, dim // 2):

        for i in range(1, dim + 1):
            # Sorteio da posicao da segunda peca com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

            # Sorteio da posicao da segunda peca com valor 'i'
            maximo = len(posicoesDisponiveis)
            indiceAleatorio = random.randint(0, maximo - 1)
            rI, rJ = posicoesDisponiveis.pop(indiceAleatorio)

            tabuleiro[rI][rJ] = -i

    return tabuleiro


def imprimeTabuleiro(tabuleiro):
    """ Imprime estado atual do tabuleiro. """

    limpaTela()

    # Imprime coordenadas horizontais
    dim = len(tabuleiro)
    print("     ", end="")
    for i in range(0, dim):
        print("{0:2d} ".format(i), end="")

    print("\n")

    # Imprime separador horizontal
    print("-----", end="")
    for i in range(0, dim):
        print("---", end="")

    print("\n")

    for i in range(0, dim):

        # Imprime coordenadas verticais
        print("{0:2d} | ".format(i), end="")

        # Imprime conteudo da linha 'i'
        for j in range(0, dim):

            # Peca ja foi removida?
            if tabuleiro[i][j] == '-':

                # Sim.
                print(" - ", end="")

            # Peca esta levantada?
            elif tabuleiro[i][j] >= 0:

                # Sim, imprime valor.
                print("{0:2d} ".format(tabuleiro[i][j]), end="")

            else:

                # Nao, imprime '?'
                print(" ? ", end="")

        print("\n")

def fechaPeca(tabuleiro, i, j):
    """ Fecha peca na posicao (i, j).
        Se posicao ja esta fechada ou se ja foi removida, retorna False.
        Caso contrario, retorna True. """

    if tabuleiro[i][j] == '-':
        return False

    elif tabuleiro[i][j] > 0:
        tabuleiro[i][j] = -tabuleiro[i][j]
        return True

    return False


def removePeca(tabuleiro, i, j):
    """ Remove peca na posicao (i, j).
        Se posicao ja esta removida, retorna False.
        Caso contrario, retorna True. """

    if tabuleiro[i][j] == '-':
        return False

    else:
        tabuleiro[i][j] = "-"
        return True


# FUNCOES DE MANIPULACAO DO PLACAR


def novoPlacar(nJogadores):
    """ Cria um novo placar zerado """

    return [0] * nJogadores


def incrementaPlacar(placar, jogador):
    """ Adiciona um ponto no placar para o jogador especificado """

    placar[jogador] = placar[jogador] + 1


def imprimePlacar(placar):
    """ Imprime o placar atual """

    nJogadores = len(placar)

    print("Placar:")
    print("---------------------")
    for i in range(0, nJogadores):
        print("Jogador {0}: {1:2d}".format(i + 1, placar[i]))


# FUNCOES DE INTERACAO COM O USUARIO


def imprimeStatus(tabuleiro, placar, vez):
    """ Imprime informacoes basicas sobre o estado atual da partida. """

    imprimeTabuleiro(tabuleiro)
    print('\n')

    imprimePlacar(placar)
    print('\n\n')

    print("Vez do Jogador {0}.\n".format(vez + 1))

host = ''
port = 7000
addr = (host, port)
# Criação do soquete do server
serv_socket = MeuSoquete()
# Definir qual IP e porta do servidor deve aguardar a conexao com algum cliente
serv_socket.sock.bind(addr)
# Aceita apenas 10 conexões
serv_socket.sock.listen(10)

print('aguardando conexao')
con, cliente = serv_socket.sock.accept()

print('conectado')
print('agurdando mensagem')
recebe = con.recv(1024)
print("mensagem recebida " + str(recebe))
serv_socket.close()
