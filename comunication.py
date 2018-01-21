from msvcrt import kbhit, getche
from select import select


class Comunication(object):
    @staticmethod
    def send(msg, client):
        rlst, wlst, elst = select.select([], [client.sock], [])
        if len(wlst) != 0:
            client.sock.send(client.name + ": " + msg)

    @staticmethod
    def recieve(sock):
        rlst, wlst, elst = select.select([sock], [], [], 0)
        data = None
        if len(rlst) != 0:
            data = sock.recv(1024)
        return data

    class KeyListener(object):
        def __init__(self, sock):
            self.message = ""
            self.sock = sock

        def key_listener(self):
            if kbhit():
                c = getche()
                if ord(c) == 13:
                    self.sock.send(self.message, self.sock)
                    self.message = ""
                    print ""
                else:
                    self.message += c
