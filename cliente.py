import socket
import struct


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

ip = 'localhost'
port = 10040
addr = (ip, port)
client_socket = socket.socket()
client_socket.connect(addr)
buffer = []

boas_vindas = recv_one_message(client_socket).decode()
print(f"{boas_vindas}")

num_sequencial = recebeDadosNumericos(recv_one_message(client_socket).decode())
coordenadas= False

dim = recebeDadosNumericos(recv_one_message(client_socket).decode())
print(f"Dimensão do tabuleiro {dim}\n")

while True:
    vez = recebeDadosNumericos(recv_one_message(client_socket).decode())

    status = recv_one_message(client_socket).decode()
    print(f"{status}")

    # Jogada de um jogador
    if num_sequencial == vez:
        # primeira peça
        while True:
            # Vale notar que eu mudei para a checagem se é uma jogada válidar ser
            # feita no cliente ao invés do servidor
            while not coordenadas:
                coordenadas = leCoordenada(dim)
            send_one_message(client_socket, coordenadas.encode())
            coordenadas = False
            peca_valida = recebeDadosNumericos(recv_one_message(client_socket).decode())
            if peca_valida == 0:
                print("Escolha uma primeira peça ainda fechada!")
                continue
            else:
                break
        
        # segunda peça
        while True:
            while not coordenadas:
                coordenadas = leCoordenada(dim)
            send_one_message(client_socket, coordenadas.encode())
            coordenadas= False
            peca_valida = recebeDadosNumericos(recv_one_message(client_socket).decode())
            if peca_valida == 0:
                print("Escolha uma segunda peçaa ainda fechada!")
                continue
            else:
                break
    #Mensagens informando as peças escolhidas 
    print(recv_one_message(client_socket).decode())
    #Mensagens informando se o jogador da vez pontuou
    print(recv_one_message(client_socket).decode())



    if not status:
        break

client_socket.close()
# client_socket2.close()
# client_socket3.close()
