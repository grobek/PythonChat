import socket
import threading
import sys


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    names = {}

    def __init__(self):
        self.sock.bind(("127.0.0.1", 9559))
        self.sock.listen(1)

    def to_someone(self, data, connections):
                data = data.split(' ')
                whoto = data[0]
                whoto = whoto[1:]
                data = ''.join(data[1:])
                if whoto in self.names.values():
                    for sock in connections:
                        sock.send(data)
                    print whoto, "exists"
                else:
                    print "tried sending to", whoto, "he doesn't exist."


    def handler(self, c, a):
        while True:
            data = str(c.recv(1024))
            if data:
                if data[0] == '@':
                    self.to_someone(data, self.connections)

                else:  # broadcast
                    for connection in self.connections:  # what to do with commands
                        if connection != c:
                            connection.send(data)
            if not data:
                print(str(self.get_name(c)[0]) , "disconnected")
                self.connections.remove(c)
                c.close()
                break


    def get_name(self, sock):
        return self.names[sock]

    def run(self):
        while True:
            c, a = self.sock.accept()
            name = c.recv(1024)

            if name in self.names.values():
                c.send("sorry, taken.")
                c.close()
                continue
            c.send("Welcome.\n")
            self.names[c] = name

            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ":" + str(a[1]), "connected")


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address):
        self.sock.connect((address, 9559))
        self.sock.send(raw_input("Enter your name: "))
        print self.sock.recv(1024)
        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print (data)

    def sendMsg(self):
        while True:  # get commands
            self.sock.send(bytes(raw_input("")))


if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()
