import os
import socket
import struct
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


def abrePeca(tabuleiro, i, j):
    """ Abre (revela) peca na posicao (i, j).
        Se posicao ja esta aberta ou se ja foi removida, retorna False.
        Caso contrario, retorna True. """

    if tabuleiro[i][j] == '-':
        return False

    elif tabuleiro[i][j] < 0:
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
    str = ''
    # limpaTela()

    # Imprime coordenadas horizontais
    dim = len(tabuleiro)
    str += "     "
    for i in range(0, dim):
        str += "{0:2d} ".format(i)

    str += "\n"

    # Imprime separador horizontal
    str += "-----"
    for i in range(0, dim):
        str += "---"

    str += "\n"

    for i in range(0, dim):

        # Imprime coordenadas verticais
        str += "{0:2d} | ".format(i)

        # Imprime conteudo da linha 'i'
        for j in range(0, dim):

            # Peca ja foi removida?
            if tabuleiro[i][j] == '-':

                # Sim.
                str += " - "

            # Peca esta levantada?
            elif tabuleiro[i][j] >= 0:

                # Sim, imprime valor.
                str += "{0:2d} ".format(tabuleiro[i][j])

            else:

                # Nao, imprime '?'
                str += " ? "

        str += "\n"
    return str


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

    str = ''
    nJogadores = len(placar)

    str += "Placar:"
    # str += "---------------------\n"
    for i in range(0, nJogadores):
        str += "Jogador {0}: {1:2d}".format(i + 1, placar[i])

    return str


# FUNCOES DE INTERACAO COM O USUARIO


def imprimeStatus(tabuleiro, placar, vez):
    """ Imprime informacoes basicas sobre o estado atual da partida. """

    str = imprimeTabuleiro(tabuleiro)
    str += '\n'

    str += imprimePlacar(placar)
    str += '\n\n'

    str += "Vez do Jogador {0}.\n".format(vez + 1)

    return str


def leCoordenada(coord):
    partes = coord.split(':')
    return int(partes[1]), int(partes[2])


# solução para evitar que mais de uma mensagem se mescle com a outra, garante que
# reciev vai receber numero fixo de dados igual ao do send

def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def main():
    # Tamanho (da lateral) do tabuleiro. Necessariamente par e menor que 10!
    dim = 4

    # Numero de jogadores por tabuleiro
    num_jogadores = 2

    host = 'localhost'
    port = 10040
    addr = (host, port)
    # Criação do soquete do server
    serv_socket = socket.socket()
    # Definir qual IP e porta do servidor deve aguardar a conexao com algum cliente
    serv_socket.bind(addr)

    # Define o tamanho max do servidor para o tamanho dos jogadores
    serv_socket.listen(num_jogadores)

    clientes = []
    while True:
        print('aguardando conexao de 2 jogadores')
        clientes.append(serv_socket.accept())
        sequencia_jogador = len(clientes) - 1
        # num_clientes_bytes = struct.pack('i', )
        # clientes[num_clientes][0].send(num_clientes)
        boas_vindas = f'Bem vindo ao servidor, jogador {sequencia_jogador}!\n'
        send_one_message(clientes[sequencia_jogador][0], boas_vindas.encode())

        num_sequencial = f"num_sequencial:{sequencia_jogador}"
        send_one_message(clientes[sequencia_jogador][0],num_sequencial.encode())

        print(f"{len(clientes)} clientes conectados")

        if len(clientes) == num_jogadores:
            break

    dados_sistema = f"dados_tabuleiro:{dim}"
    for cliente in clientes:
        send_one_message(cliente[0],dados_sistema.encode())
    # 2 clientes conectados

    # Numero total de pares de pecas
    totalDePares = dim ** 2 / 2

    # PROGRAMA PRINCIPAL

    # Cria um novo tabuleiro para a partida
    tabuleiro = novoTabuleiro(dim)

    # Cria um novo placar zerado
    placar = novoPlacar(num_jogadores)

    # Partida continua enquanto ainda ha pares de pecas a casar.
    paresEncontrados = 0
    vez = 0
    buffer = []
    while paresEncontrados < totalDePares:

        dados_vez = f"dados_vez:{vez}"
        for cliente in clientes:
            send_one_message(cliente[0], dados_vez.encode())
            send_one_message(cliente[0], imprimeStatus(tabuleiro, placar, vez).encode())


        # Jogada de um jogador

        # Solicita coordenadas da primeira peca.
        while True:
            coordenadas = recv_one_message(clientes[vez][0]).decode()
            coordenadas = leCoordenada(coordenadas)
            print(coordenadas)

            i1, j1 = coordenadas

            # Testa se peca ja esta aberta (ou removida)
            if not abrePeca(tabuleiro, i1, j1):
                erro = "peca_aberta:0"
                send_one_message(clientes[vez][0], erro.encode())
                continue
            else:
                acerto = "peca_aberta:1"
                send_one_message(clientes[vez][0], acerto.encode())
                break
        # Solicita coordenadas da primeira peca.
        while True:
            coordenadas = recv_one_message(clientes[vez][0]).decode()
            coordenadas = leCoordenada(coordenadas)
            print(coordenadas)

            i2, j2 = coordenadas

            # Testa se peca ja esta aberta (ou removida) e ve se ele não repetiu a peça anterior
            if not abrePeca(tabuleiro, i2, j2) or (i2==i1 and j1==j2):
                erro = "peca_aberta:0"
                send_one_message(clientes[vez][0], erro.encode())
                continue
            else:
                acerto = "peca_aberta:1"
                send_one_message(clientes[vez][0], acerto.encode())
                break
        
        for cliente in clientes:
            send_one_message(cliente[0], ("Pecas escolhidas pelo jogador {0} --> ({1}, {2}) e ({3}, {4})\n".format(vez, i1, j1, i2, j2)).encode())
        time.sleep(2)
         # Pecas escolhidas sao iguais?
        if tabuleiro[i1][j1] == tabuleiro[i2][j2]:
            incrementaPlacar(placar, vez)
            paresEncontrados = paresEncontrados + 1
            removePeca(tabuleiro, i1, j1)
            removePeca(tabuleiro, i2, j2)
            time.sleep(2)
            for cliente in clientes:
                send_one_message(cliente[0], ("Pecas casam! Ponto para o jogador {0}.".format(vez + 1)).encode())
        else:
            fechaPeca(tabuleiro, i1, j1)
            fechaPeca(tabuleiro, i2, j2)
            time.sleep(3)
            for cliente in clientes:
                send_one_message(cliente[0], ("Pecas do jogador {0} nao casam!".format(vez + 1)).encode())
        
        #troca a vez e repete o loop
        vez = (vez + 1) % 2
    # #

    # #
    # # # Verificar o vencedor e imprimir
    # # pontuacaoMaxima = max(placar)
    # # vencedores = []
    # # for i in range(0, nJogadores):
    # #
    # #     if placar[i] == pontuacaoMaxima:
    # #         vencedores.append(i)
    # #
    # # if len(vencedores) > 1:
    # #
    # #     print("Houve empate entre os jogadores ")
    # #     for i in vencedores:
    # #         print(str(i + 1) + ' ')
    # #
    # #     print("\n")
    # #
    # # else:
    # #     print("Jogador {0} foi o vencedor!".format(vencedores[0] + 1))
    serv_socket.close()


main()
