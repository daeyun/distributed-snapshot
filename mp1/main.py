#!/usr/bin/env python3
import logging
import sys
import multiprocessing as mp
import random
from helpers.networking_helper import pick_free_ports
from trader_process import *
from helpers.file_io_helper import delete_snapshots
from helpers.trading_helper import get_initial_trading_vars

logger = logging.getLogger()


def run():
    logger.info("Master process started")

    rand = random.Random()
    rand.seed(0)

    processes = []
    n_processes = 5
    ports = pick_free_ports(n_processes * (n_processes - 1))

    port_mapping = {}
    counter = 0
    for i in range(n_processes):
        for j in range(i + 1, n_processes):
            port_mapping[(i, j)] = (ports[counter], ports[counter + 1])
            counter = counter + 2

    num_snapshots = 5
    widget = 0
    money = 0
    for i in range(n_processes):
        asset = get_initial_trading_vars(rand)
        widget = widget + asset[0]
        money = money + asset[1]
        p = mp.Process(target=trader_process, args=(port_mapping, n_processes, i, asset, num_snapshots))
        p.start()
        processes.append(p)

    print("Widget: ", widget, "Money: ", money)

    for p in processes:
        p.join()



if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s]"
                                  "[%(levelname)-5.5s]  %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        delete_snapshots()
        run()
    except:
        logger.exception("Unexpected error")
