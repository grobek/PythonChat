import socket
import select
import sys


class ChatClient(object):
    def __init__(self, name, host='127.0.0.1', port=9955):
        self.port = int(port)
        self.name = name
        self.host = host
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            # Send my name...
            while not self.check_name():
                self.name = raw_input(self.name + " Is not available.\n Enter your name: ")
            print 'Connected to chat server@%d as %s' % (self.port, self.name)
            # Initial prompt
            self.prompt = '[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']> '
            # Contains client address, set it
            data = self.sock.recv(1024)
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error:
            print 'Could not connect to chat server @%d' % self.port
            sys.exit(1)

    def run(self):
        command = ""
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        inputs = [self.sock, sock2]
        # TODO program has started getting stuck on this line for no reason (line 34)
        ready_to_read, ready_to_write, in_error = select.select(inputs, [], [])
        while "/exit" not in command:
            for i in ready_to_read:
                if i != self.sock:
                    print 'write what you want\n write /help for help'
                    command = raw_input()
                    if "/help" in command[:5]:
                        print "A dot indicates the end of the syntax, {x} are neccesary arguements."
                        print "The commands available to you and their syntax:"
                        print "/exit. Exit the chat"
                        print "/help. View this menu"
                        print "/send {user_dest} {data}. Send a message, {user_dest} can also be broadcast " \
                              "(send to everyone) if it is wished."
                        print "-----------------------"
                    elif "/sendall" in command[:8]:
                        command = command.replace("/sendall", "")
                        self.sock.send("broadcast" + command)
                    elif "/send" in command[:5]:
                        command = command.replace("/send", "")
                        self.sock.send(command)
                elif i == self.sock:
                    data = self.sock.recv(1024)
                    if data:
                        print data + '   *'
        self.exit()

    def exit(self):
        self.sock.send("bye")
        self.sock.close()

    def check_name(self):
        self.sock.send("/name " + self.name)
        data = self.sock.recv(1024)
        print str(data+"////////////////")
        print str(data)
        print str(data)
        if str(data) == 'ok':
            self.sock.send("something")
        return 'ok' in str(data)


if __name__ == '__main__':
    namee = raw_input("Please enter your name: ")
    me = ChatClient(namee)
    me.run()
