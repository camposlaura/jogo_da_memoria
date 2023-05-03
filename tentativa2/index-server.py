import threading
import socket
import JogoDaMemoria as jm

clients = []
dim = 4
nr = 2
def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7777))
        server.listen(nr)
    except:
        return print('\nNão foi possível iniciar o servidor!\n')
    
    tabuleiro = jm.novoTabuleiro(dim)
    placar = jm.novoPlacar(nr)
    vez = 0
    while True:
        client, addr = server.accept()
        clients.append(client)
        x = jm.imprimeStatus(tabuleiro, placar, vez)
        broadcast(x,server)
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            broadcast(msg, client)
        except:
            deleteClient(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)


def deleteClient(client):
    clients.remove(client)

main()