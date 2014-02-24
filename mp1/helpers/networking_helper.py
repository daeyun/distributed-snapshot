import socket


def pick_free_ports(n):
    """return a list of n free port numbers. https://www.dnorth.net/2012/03/17/the-port-0-trick/"""
    ports = []
    sockets = []

    for i in range(n):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        _, port = s.getsockname()
        sockets.append(s)
        ports.append(port)

    for s in sockets:
        s.close()

    return ports