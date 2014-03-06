import struct
import math

def get_initial_trading_vars(rand):
    widgets = rand.randint(100, 400)
    money = rand.randint(1200, 2500)
    return [widgets, money]

def unpack_list_data(struct_list):
    int_list_len = int(len(struct_list)/4)
    int_list = []
    for i in range(int_list_len):
        int_list.append(struct.unpack('!i', struct_list[i * 4 : i * 4 + 4])[0])

    return int_list

def update_logical_timestamp(local_timestamp, received_timestamp):
    return max(local_timestamp, received_timestamp) + 1

def update_vector_timestamp(local_timestamp, received_timestamp):
    new_timestamp = [0] * len(local_timestamp)
    for i in range(len(local_timestamp)):
        new_timestamp[i] = max(local_timestamp[i], received_timestamp[i])
    return new_timestamp