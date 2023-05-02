import os
import socket
import sys
import time
import random


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


def main():
    # Tamanho (da lateral) do tabuleiro. Necessariamente par e menor que 10!
    dim = 4

    # Numero de jogadores por tabuleiro
    num_jogadores = 2

    host = 'localhost'
    port = 9000
    addr = (host, port)
    # Criação do soquete do server
    serv_socket = socket.socket()
    # Definir qual IP e porta do servidor deve aguardar a conexao com algum cliente
    serv_socket.bind(addr)

    # Define o tamanho max do servidor para o tamanho dos jogadores
    serv_socket.listen(num_jogadores)

    num_clientes = 0
    cliente = []
    while True:
        print('aguardando conexao de 2 jogadores')
        cliente.append(serv_socket.accept())
        print(f"Conexão estabelecida com {cliente[num_clientes][1]}")
        boas_vindas = "Bem vindo ao servidor!"
        cliente[num_clientes][0].send(boas_vindas.encode())
        num_clientes += 1
        print(f"{num_clientes} clientes conectados")

        if num_clientes == num_jogadores:
            break

    # 2 clientes conectados
    serv_socket.close()

    #
    # Numero total de pares de pecas
    totalDePares = dim ** 2 / 2
    #
    # PROGRAMA PRINCIPAL
    #
    # Cria um novo tabuleiro para a partida
    tabuleiro = novoTabuleiro(dim)
    # #
    # # Cria um novo placar zerado
    # placar = novoPlacar(num_jogadores)
    # #
    # # Partida continua enquanto ainda ha pares de pecas a casar.
    # paresEncontrados = 0
    # vez = 0
    # while paresEncontrados < totalDePares:
    #
    #     # Requisita primeira peca do proximo jogador
    #     while True:
    #         # Imprime status do jogo
    #         imprimeStatus(tabuleiro, placar, vez)
    #
    #         # Solicita coordenadas da primeira peca.
    #         coordenadas = leCoordenada(dim)
    #         if not coordenadas:
    #             continue
    #
    #         i1, j1 = coordenadas
    #
    #         # Testa se peca ja esta aberta (ou removida)
    #         if not abrePeca(tabuleiro, i1, j1):
    #             print("Escolha uma peca ainda fechada!")
    #             input("Pressione <enter> para continuar...")
    #             continue
    #
    #         break
    #
    #         # Requisita segunda peca do proximo jogador
    #     while True:
    #
    #         # Imprime status do jogo
    #         imprimeStatus(tabuleiro, placar, vez)
    #
    #         # Solicita coordenadas da segunda peca.
    #         coordenadas = leCoordenada(dim)
    #         if not coordenadas:
    #             continue
    #
    #         i2, j2 = coordenadas
    #
    #         # Testa se peca ja esta aberta (ou removida)
    #         if not abrePeca(tabuleiro, i2, j2):
    #             print("Escolha uma peca ainda fechada!")
    #             input("Pressione <enter> para continuar...")
    #             continue
    #
    #         break
    #
    #         # Imprime status do jogo
    #     imprimeStatus(tabuleiro, placar, vez)
    #
    #     print("Pecas escolhidas --> ({0}, {1}) e ({2}, {3})\n".format(i1, j1, i2, j2))
    #
    #     # Pecas escolhidas sao iguais?
    #     if tabuleiro[i1][j1] == tabuleiro[i2][j2]:
    #
    #         print("Pecas casam! Ponto para o jogador {0}.".format(vez + 1))
    #
    #         incrementaPlacar(placar, vez)
    #         paresEncontrados = paresEncontrados + 1
    #         removePeca(tabuleiro, i1, j1)
    #         removePeca(tabuleiro, i2, j2)
    #
    #         time.sleep(5)
    #
    #     else:
    #
    #         print("Pecas nao casam!")
    #
    #         time.sleep(3)
    #
    #         fechaPeca(tabuleiro, i1, j1)
    #         fechaPeca(tabuleiro, i2, j2)
    #         vez = (vez + 1) % nJogadores
    #
    # # Verificar o vencedor e imprimir
    # pontuacaoMaxima = max(placar)
    # vencedores = []
    # for i in range(0, nJogadores):
    #
    #     if placar[i] == pontuacaoMaxima:
    #         vencedores.append(i)
    #
    # if len(vencedores) > 1:
    #
    #     print("Houve empate entre os jogadores ")
    #     for i in vencedores:
    #         print(str(i + 1) + ' ')
    #
    #     print("\n")
    #
    # else:
    #
    #     print("Jogador {0} foi o vencedor!".format(vencedores[0] + 1))


main()
