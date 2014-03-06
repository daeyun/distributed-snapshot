import os
import socket
import struct
from unittest import TestCase
import sys
from mp1.mp1.helpers.networking_helper import pick_free_ports
from mp1.mp1.helpers.trading_helper import unpack_list_data


class TestTradingHelpers(TestCase):
    def test_unpack_list_data(self):

        packed_int_list = b''
        num = 7
        int_list = [0, 5, 1, 2, 3, 4, 5]
        for i in range(num):
            packed_int_list = packed_int_list + struct.pack('!i', int_list[i])

        unpacked_list = unpack_list_data(packed_int_list)

        self.assertEqual(len(unpacked_list), num)

        for i in range(num):
            self.assertEqual(unpacked_list[i], int_list[i])


