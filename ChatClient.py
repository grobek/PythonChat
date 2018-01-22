import socket
import select
import sys
from comunication import Comunication as c

class ChatClient(object):
    def __init__(self, name, host='127.0.0.1', port=9955):
        self.port = int(port)
        self.name = name
        self.host = host
        # Connect to server at port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            # Send my name...
            while not self.check_name():
                self.name = raw_input(self.name + " Is not available.\n Enter your name: ")
            print 'Connected to chat server@%d as %s' % (self.port, self.name)

        except socket.error:
            print 'Could not connect to chat server @%d' % self.port
            sys.exit(1)

    def help(self):
        print "A dot indicates the end of the syntax, {x} are neccesary arguements."
        print "The commands available to you and their syntax:"
        print "/exit. Exit the chat"
        print "/help. View this menu"
        print "/send {user_dest} {data}. Send a message, {user_dest} can also be broadcast " \
              "/sendall {data}.(send to everyone) if it is wished."
        print "/getnames. prints all online memebers"
        print "-----------------------"

    def run(self):
        while "/exit" not in command:
            command = ""

            empty_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            inputs = [self.sock, empty_sock]
            ready_to_read, ready_to_write, in_error = select.select(inputs, [], [])

            for i in ready_to_read:
                if i == self.sock:
                    data = c.recieve(self.sock)
                    if data:
                        print data + '   *'

                else:#if i != self.sock:
                    print 'write what you want\n write /help for help'
                    lForKey = c.KeyListener(self.sock)
                    command = lForKey.key_listener()
                    if "/help" in command[:5]:
                        self.help()
                    elif "/sendall" in command[:8]:
                        command = command.replace("/sendall", "")
                        c.send("broadcast" + command, self.sock)#self.sock.send("broadcast" + command)
                    elif "/send" in command[:5]:
                        command = command.replace("/send", "")
                        c.send(command, self.sock)#self.sock.send(command)
                    elif "/getnames" in command:
                        c.send("/getnames", self.sock)
                        rec = c.recieve(self.sock)
                        print rec  # print the names

        self.exit()

    def exit(self):
        c.send("bye", self.sock)
        self.sock.close()

    def check_name(self):
        self.sock.send("/name " + self.name)
        data = c.recieve(self.sock)
        if str(data) == 'ok':
            c.send("something", self.sock)
        return 'ok' in str(data)


if __name__ == '__main__':
    namee = raw_input("Please enter your name: ")
    me = ChatClient(namee)
    me.run()

