import socket
SERVER_IP = ""
PORT = 0


class ChatClient(object): 
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((SERVER_IP, int(PORT)))
        names = ChatClient.request_names()
        self.name = raw_input("Enter your name: ")
        while self.name not in names and self.name[0] is not '/':
            self.name = raw_input(self.name + "Is not available.\n Enter your name: ")

    # TODO immediately after connection established send name
    def run(self):
        command = ""
        while "/exit" not in command:
            if "/help" in command[:5]:
                print "A dot indicates the end of the syntax, {x} are neccesary arguements."
                print "The commands available to you and their syntax:"
                print "/exit. Exit the chat"
                print "/help. View this menu"
                print "/send {user_dest} {data}. Send a message, {user_dest} can also be broadcast (send to everyone) if it is wished."
                print "-----------------------"
            elif "/sendall in command[:8]":
                command = command.replace("/sendall", "")
                data = command.strip()
                self.send("broadcast", data)
            elif "/send" in command[:5]:
                self.sock.send(command)
            # TODO
            command = raw_input()

        self.exit()

    def exit(self):
        self.socket.close()

    @staticmethod
    def request_names(self):
        self.sock.send("/names")
        return self.sock.recv(1024)


if __name__ == '__main__':
    me = ChatClient()
    me.run()
