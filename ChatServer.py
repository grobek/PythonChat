import socket
import select


class ChatServer:
    def __init__(self, port=9955, ip=''):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ip, port)
        self.online = []
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
                if sock == self.server:
                    sockfd, addr = self.server.accept()
                    self.online.append(sockfd)
                    print "Client (%s, %s) connected" % addr