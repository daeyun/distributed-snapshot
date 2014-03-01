import socket
from mp1.mp1.main import logger

def trader_process(port_mapping, n_processes, id):
    # logger.info("Process id: ", id)
    sockets = []
    backlog = 10

    for i in range(id):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(socket.gethostname(), port_mapping[(i, id)][1])
        server_sock.listen(backlog)
        client_sock, (host, client_port) = server_sock.accept()
        sockets.append(server_sock)

    sockets.append(None)

    for i in range(id + 1, n_processes):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.gethostname()
        (source_port, destination_port) = port_mapping[(id, i)]
        client_sock.bind((addr, source_port))
        client_sock.connect((addr, destination_port))
        sockets.append(client_sock)

    pass
