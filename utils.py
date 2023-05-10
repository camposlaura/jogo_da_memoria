import struct


def envia_mensagem(sock, data):
    """Envia uma mensagem para um socket com cabeçalho contendo o tamanho da mensagem."""
    length = len(data)
    sock.sendall(struct.pack("!I", length))
    sock.sendall(data)


def recebe_mensagem(sock):
    """Le o tamanho do cabeçalho para saber o tamanho exato da mensagem a ser recebida."""
    lengthbuf = recvall(sock, 4)
    (length,) = struct.unpack("!I", lengthbuf)
    return recvall(sock, length)


def recvall(sock, count):
    """Funcao auxiliar de recebe_mensagem(sock). Cria um buffer para garantir que a mensagem seja recebida sem que nenhum bit seja perdido no processo."""
    buf = b""
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf
