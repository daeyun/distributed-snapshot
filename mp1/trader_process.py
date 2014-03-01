import socket
import random
import struct
from mp1.mp1.helpers.trading_helper import unpack_list_data
from mp1.mp1.main import logger

def trader_process(port_mapping, n_processes, id, asset):
    rand = random.Random()
    rand.seed(id)
    buying_probability = rand.uniform(0.01, 0.1)

    sockets = []
    backlog = 10

    types = {
        'send_money': 0,
        'send_widget': 1,
    }
    inv_types = {v:k for k, v in types.items()}

    def send_int_list(dest_pid, type, int_list):
        sock = sockets[dest_pid]
        message = struct.pack('!i', type) + struct.pack('!i', len(int_list))

        for item in int_list:
            message = message + struct.pack('!i', item)

        sock.sendall(message)

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
                type = struct.unpack('!i', sockets[i].recv[4])[0]
                if inv_types(type) == 'send_money':
                    num_items = struct.unpack('!i', sockets[i].recv[4])[0]
                    int_list = unpack_list_data(sockets[i].recv[num_items * 4])

                    money_received = int_list[0]
                    asset[1] = asset[1] + money_received

                    print(id, 'received $', money_received, ' from process ', i)

                    widgets_sending = buying_amount # assuming 1 widget costs 1 money
                    send_int_list(i, types['send_widget'], [widgets_sending])
                elif inv_types(type) == 'send_widget':
                    num_items = struct.unpack('!i', sockets[i].recv[4])[0]
                    int_list = unpack_list_data(sockets[i].recv[num_items * 4])

                    widgets_received = int_list[0]
                    asset[0] = asset[0] + widgets_received

                    print('Received ', widgets_received, ' widgets from process ', i)
                else:
                    print("Unknown type error")
                    raise Exception("Unknown type error")

            except socket.timeout:
                pass
            except BlockingIOError:
                pass

        # sending message
        buying_attempt = rand.uniform(0, 1)
        if buying_attempt <= buying_probability:
            seller = rand.randint(0, n_processes - 2)

            if seller >= id:
                seller = seller + 1

            current_money = asset[1]
            if current_money == 0:
                pass
            else:
                buying_amount = rand.randint(1, int(current_money/3)+1)
                asset[1] = asset[1] - buying_amount
                send_int_list(seller, types['send_money'], [buying_amount])
