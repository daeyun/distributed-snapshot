import socket
import random
import struct
from mp1.mp1.helpers.trading_helper import unpack_list_data
from mp1.mp1.helpers.trading_helper import update_logical_timestamp
from mp1.mp1.helpers.trading_helper import update_vector_timestamp
from mp1.mp1.main import logger

def trader_process(port_mapping, n_processes, id, asset):
    rand = random.Random()
    rand.seed(id)
    sending_probability = rand.uniform(0.005, 0.05)

    sockets = []
    backlog = 10

    types = {
        'send_money': 0,
        'send_widget': 1,
    }
    inv_types = {v:k for k, v in types.items()}

    logical_timestamp = 0
    vector_timestamp = [0] * n_processes

    # send a message to process dest_pid
    def send_int_list(dest_pid, type, int_list):
        sock = sockets[dest_pid]
        message = struct.pack('!i', type) + struct.pack('!i', len(int_list))

        for item in int_list:
            message = message + struct.pack('!i', item)

        sock.sendall(message)

    # initialize sockets
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

    # set timeouts for sockets
    for i in range(n_processes):
        if i == id:
            continue
        sockets[i].settimeout(0.01)

    # main logic loop
    while True:
        # receiving money (sending widgets)
        for i in range(n_processes):
            if i == id:
                continue

            try:
                data = sockets[i].recv(4)
                if len(data) == 0:
                    continue

                type = struct.unpack('!i', data)[0]
                if inv_types[type] == 'send_money':
                    num_items = struct.unpack('!i', sockets[i].recv(4))[0]
                    int_list = unpack_list_data(sockets[i].recv(num_items * 4))

                    money_received = int_list[0]
                    logical_timestamp_received = int_list[1]
                    vector_timestamp_received = int_list[2:]

                    # update timestamps
                    logical_timestamp = update_logical_timestamp(logical_timestamp, logical_timestamp_received)
                    vector_timestamp[id] = vector_timestamp[id] + 1
                    vector_timestamp = update_vector_timestamp(vector_timestamp, vector_timestamp_received)

                    # update money
                    asset[1] = asset[1] + money_received

                    print(id, 'received ', money_received, ' dollars from process ', i, asset)
                    print(id, ' received ', logical_timestamp, ' ', vector_timestamp)
                elif inv_types[type] == 'send_widget':
                    num_items = struct.unpack('!i', sockets[i].recv(4))[0]
                    int_list = unpack_list_data(sockets[i].recv(num_items * 4))

                    widgets_received = int_list[0]
                    logical_timestamp_received = int_list[1]
                    vector_timestamp_received = int_list[2:]

                    # update timestamps
                    logical_timestamp = update_logical_timestamp(logical_timestamp, logical_timestamp_received)
                    vector_timestamp[id] = vector_timestamp[id] + 1
                    vector_timestamp = update_vector_timestamp(vector_timestamp, vector_timestamp_received)

                    # update widgets
                    asset[0] = asset[0] + widgets_received

                    print(id, ' received ', logical_timestamp, ' ', vector_timestamp)
                    print(id, 'received ', widgets_received, ' widgets from process ', i, asset)
                else:
                    print("Unknown type error")
                    raise Exception("Unknown type error")

            except socket.timeout:
                pass
            except BlockingIOError:
                pass

        # sending money (buying widgets)
        buying_attempt = rand.uniform(0, 1)
        if buying_attempt <= sending_probability:
            seller = rand.randint(0, n_processes - 2)

            if seller >= id:
                seller = seller + 1

            if rand.randint(0, 1) == 0:
                # send money
                current_money = asset[1]
                if current_money <= 0:
                    pass
                else:
                    buying_amount = rand.randint(1, int(current_money/3)+1)
                    asset[1] = asset[1] - buying_amount
                    logical_timestamp = logical_timestamp + 1
                    vector_timestamp[id] = vector_timestamp[id] + 1
                    print(id, ' send money ', logical_timestamp, ' ', vector_timestamp)
                    send_int_list(seller, types['send_money'], [buying_amount, logical_timestamp] + vector_timestamp)
            else:
                # send widget
                current_widget = asset[0]
                if current_widget <= 0:
                    pass
                else:
                    buying_amount = rand.randint(1, int(current_widget/3)+1)
                    asset[0] = asset[0] - buying_amount
                    logical_timestamp = logical_timestamp + 1
                    vector_timestamp[id] = vector_timestamp[id] + 1
                    print(id, ' send widget ', logical_timestamp, ' ', vector_timestamp)
                    send_int_list(seller, types['send_widget'], [buying_amount, logical_timestamp] + vector_timestamp)
