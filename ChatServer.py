import socket
import select


class ChatServer:
    def __init__(self, port=9955, ip=''):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ip, port)
        self.online = []
        self.names = []
        print "Server is up, now listening..."
        self.server.listen(10)

    def run(self):
        # add server socket object to the list of readable connections
        self.online.append(self.server)
        print "Chat server started "
        while 1:
            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read, ready_to_write, in_error = select.select(self.online, [], [], 0)
            for sock in ready_to_read:
                # new connection
                if sock == self.server:
                    sockfd, addr = self.server.accept()
                    self.online.append(sockfd)
                    # TODO
                    self.names.append(self.server.recv(2048))
                    print "Client (%s, %s) connected" % addr
                    self.broadcast("Client (%s, %s) connected" % addr)
                # a message
                # TODO
                else:
                    try:
                        data = self.server.recv(2048)
                        data = data.replace("/send", "")
                        data = data.strip()
                        arg1 = str(data[:data.index(" ")])
                        arg2 = str(data[data.index(" ") + 1:])
                        self.send(arg1, arg2)
                    except:
                        self.server.send("sorry, " + " is not connected")

    # TODO
    def broadcast(self, msg):
        ready_to_read, ready_to_write, in_error = select.select(self.online, [], [], 0)
        for sock in ready_to_read:
            sock.send(msg)
