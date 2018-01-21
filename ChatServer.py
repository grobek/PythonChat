import socket
import select
from comunication import Comunication as c


class ChatServer(object):
    def __init__(self, port=9955, host='127.0.0.1'):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.online = []
        self.names = {}
        print "Server is up, now listening..."
        self.server.listen(10)

    def getname(self, client):
        # Return the printable name of the
        # client, given its socket...
        info = self.names[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def run(self):
        # add server socket object to the list of readable connections
        self.online.append(self.server)
        print "Chat server started "
        while 1:
            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read, ready_to_write, in_error = select.select(self.online, [], [], 0)
            for s in ready_to_read:
                # new connection
                if s == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print 'chatserver: got connection %d from %s' % (client.fileno(), address)
                    # Read the login name
                    cname = c.recieve(client).split('/name ')[1]
                    while cname in self.names.values():
                        c.send("this name is taken", client)
                        cname = c.recieve(client).split('/name ')[1]
                    client.send("ok")
                    client.recv(1024)
                    print cname
                    # Compute client name and send back
                    client.send('CLIENT: ' + str(address[0]))
                    self.online.append(client)

                    self.names[client] = cname
                    # Send joining information to other clients
                    msg = '\n(Connected: New client %s)' % (self.getname(client))
                    print "Client (%s, %s) connected" % address
                    self.broadcast("Client (%s) connected" % msg, 'SERVER')
                # a message
                else:
                    data = str(c.recieve(s)).split()
                    if data[0] == '/getnames':
                        print str(self.names.values()) + "ABCEDFGHIJK"
                        s.send(str(self.names.values()))
                    else:
                        print data
                        if data[0] == 'broadcast':
                            data.remove(data[0])
                            self.broadcast(' '.join(data), self.getname(s))
                        elif data[0] in self.names.values():
                            for cl in self.names.keys():
                                if self.names[cl] == data[0] and cl in self.online:
                                    data.remove(data[0])
                                    cl.send(' '.join(data))
                                    break
                            cl.send(self.getname(cl) + ' is offline')
                        elif data[0] == 'bye':
                            self.online.remove(s)
                            self.broadcast(self.names[s] + " have disconnected", 'SERVER')
                            del self.names[s]
                            s.close()
                            
                        else:  # if name not in self.names.value()
                            print str(data[0]) + ' is offline'
    
    def broadcast(self, msg, name):
        ready_to_read, ready_to_write, in_error = select.select([], self.online, [])
        for sock in ready_to_read:
            sock.send(name + ': ' + msg)

if __name__ == "__main__":
    ChatServer().run()
