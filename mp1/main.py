#!/usr/bin/env python3
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s]"
                              "[%(levelname)-5.5s]  %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def run():
    logger.info("Hello")

if __name__ == '__main__':
    try:
        run()
    except:
        logger.exception("Unexpected error")