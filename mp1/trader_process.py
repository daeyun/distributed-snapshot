import socket
import random
from mp1.mp1.main import logger

def trader_process(port_mapping, n_processes, id, asset):
    rand = random.Random()
    rand.seed(id)
    buying_probability = rand.uniform(0.01, 0.1)

    sockets = []
    backlog = 10

    def send_message(dest_pid, message):
        sock = sockets[dest_pid]
        sock.send(str(message).encode('utf'))

    for i in range(id):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((socket.gethostname(), port_mapping[(i, id)][1]))
        server_sock.listen(backlog)
        client_sock, (host, client_port) = server_sock.accept()
        sockets.append(client_sock)

    sockets.append(None)

    for i in range(id + 1, n_processes):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.gethostname()
        (source_port, destination_port) = port_mapping[(id, i)]
        client_sock.bind((addr, source_port))
        client_sock.connect((addr, destination_port))
        sockets.append(client_sock)

    for i in range(id):
        sockets[i].settimeout(0.01)

    while True:
        # receiving message
        for i in range(id):
            try:
                data = sockets[i].recv(1024)
                print(data)
            except socket.timeout:
                pass
            except BlockingIOError:
                pass

        # sending message
        buying_attempt = rand.uniform(0, 1)
        if buying_attempt <= buying_probability:
            seller = rand.randint(0, n_processes - 1)
            if seller >= id:
                seller = seller + 1

            current_money = asset[1]
            if current_money == 0:
                pass
            else:
                buying_amount = rand.randint(1, current_money)
                send_message(seller, buying_amount)
    pass
