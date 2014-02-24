import os
import socket
from unittest import TestCase
import sys
from mp1.mp1.helpers.networking_helper import pick_free_ports


class TestNetworkingHelpers(TestCase):
    def test_pick_free_ports_length(self):
        ports = pick_free_ports(5)
        self.assertEqual(len(ports), 5)

    def test_pick_free_ports_distinct(self):
        ports = pick_free_ports(20)
        seen = {}

        for port in ports:
            self.assertFalse(port in seen)
            seen[port] = True

    def test_pick_free_ports_available(self):
        port = pick_free_ports(1)[0]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', port))
        _, assigned_port = s.getsockname()
        self.assertEqual(port, assigned_port)
