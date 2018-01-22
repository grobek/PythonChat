import socket
import select
from comunication import Comunication as c


class ChatServer(object):
    def __init__(self, port=9955, host='127.0.0.1'):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\
        self.server.bind((host, port))
        self.online = []
        self.names = {}
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
                    new_sock, address = self.server.accept()


                    print 'chatserver: got connection. IP: %s' % address
                    cname = new_sock.recv(1024).split('/name ')[1]
                    while cname in self.names.values():
                        c.send("this name is taken", new_sock)
                        cname = new_sock.recv(1024).split('/name ')[1]
                    new_sock.send("ok")
                    new_sock.recv(1024)
                    print cname
                    #new_sock.send('CLIENT: ' + str(address[0]))\

                    self.online.append(new_sock)

                    self.names[new_sock] = cname
                    # Send joining information to other clients
                    msg = '\n(Connected: New client %s)' % (self.getname(new_sock))
                    print "Client (%s, %s) connected" % address

                    self.broadcast("Client (%s) connected" % msg, 'SERVER')
                # a message
                else:
                    try:
                        data = str(c.recieve(sock)).split()
                        if data:
                            if data[0] == '/getnames':
                                print str(self.names.values())
                                sock.send(str(self.names.values()))
                            else:
                                print data
                                if data[0] == 'broadcast': # to all
                                    data.remove(data[0])
                                    self.broadcast(' '.join(data), self.getname(sock))
                                elif data[0] in self.names.values(): # to someone specific
                                    for cl in self.names.keys():
                                        if self.names[cl] == data[0] and cl in self.online:
                                            data.remove(data[0])
                                            cl.send(' '.join(data))
                                            break
                                    cl.send(self.getname(cl) + ' is offline')
                                elif data[0] == 'bye': # exit message
                                    self.online.remove(sock)
                                    self.broadcast(self.names[sock] + " have disconnected", 'SERVER')
                                    del self.names[sock]
                                    sock.close()

                                else:  # if name not in self.names.value()
                                    print str(data[0]) + ' is offline'
                        else: # someone has disconnected
                            if sock in self.online:
                                self.online.remove(sock)
                            self.broadcast(self.getname(sock) + ": have disconnected", 'SERVER')
                    except:
                        self.broadcast(self.getname(sock) + ": have disconnected", 'SERVER')
                        continue
    
    def broadcast(self, msg, name):
        ready_to_read, ready_to_write, in_error = select.select([], self.online, [])
        for sock in ready_to_read:
            try: # try to send
                sock.send(name + ': ' + msg)
            except: # broken socket or something
                sock.close()
                del self.names[sock]
                self.online.remove(sock)

    def getname(self, client):
        # Return the printable name of the
        # client, given its socket...
        info = self.names[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

if __name__ == "__main__":
    ChatServer().run()

