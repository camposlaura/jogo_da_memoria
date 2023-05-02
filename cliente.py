import socket


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

    return f"{i}, {j}"


ip = 'localhost'
port = 10000
addr = (ip, port)
client_socket = socket.socket()
client_socket.connect(addr)
client = client_socket.recv(16392)
print(f"{client}")

# client = client_socket.recv(4098)
# print(f"{client}")
# client_socket.send(leCoordenada().encode())

client_socket.close()
# client_socket2.close()
# client_socket3.close()
