import socket
import threading
import sys


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    names = {}

    def __init__(self):
        self.sock.bind(("10.100.102.2", 9559))
        self.sock.listen(1)

    def to_someone(self, data, connections, sock_source):
                data = data.split(' ')
                whoto = data[0]
                whoto = whoto[1:]
                data = ' '.join(data[1:])
                if whoto in self.names.values():
                    for sock in connections:
                        if self.get_name(sock) == whoto:
                            sock.send("PM FROM @" + self.get_name(sock_source) + ": " + data)
                    print whoto, "exists"
                else:
                    print "tried sending to", whoto, "he doesn't exist."


    def handler(self, c, a):
        while True:
            data = str(c.recv(1024))
            if data:
                if data == '@?':
                    c.send("ONLINE: " + str(self.names.values()))
                elif data[0] == '@':
                    self.to_someone(data, self.connections, c)
                else:  # broadcast
                    print "@" + self.get_name(c), "broadcasted:", data
                    for connection in self.connections:  # what to do with commands
                        if connection != c:
                            connection.send("BROADCAST FROM @" + self.get_name(c) + ": " + data)
            if not data:
                for connection in self.connections:  # what to do with commands
                    if connection != c:
                        connection.send("User " + self.get_name(c) + " has disconnected")
                print(str(self.get_name(c)) , "disconnected")
                del self.names[c]
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
            for connection in self.connections:  # what to do with commands
                if connection != c:
                    connection.send("User " + self.get_name(c), "has connected")
            print(str(self.get_name(c)), "disconnected")


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

    def help(self):
        print "USES:"
        print "[data] to broadcast"
        print "@[someone] [data] to PM"
        print "@? to get list of online users"
        print "?? to print this manual"
        print "!! to exit"

    def sendMsg(self):
        self.help()
        keep = True
        while True:  # get commands
            commands = raw_input("")
            if commands == '??':
                self.help()
            elif commands == '!!':
                self.sock.close()
                sys.exit(0)
            else:
                self.sock.send(commands)


if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()
