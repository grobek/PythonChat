import socket
SERVER_IP = ""
PORT = 0


class ChatClient(object): 
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((SERVER_IP, int(PORT)))

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
                command = command.replace("/send", "")
                command = command.strip()
                arg1 = str(command[:command.index(" ")])
                arg2 = str(command[command.index(" ") + 1:])
                self.send(arg1, arg2)

            command = raw_input()

        self.exit()

    def send(self, dest, content):
        self.sock.send(str(dest + ":" + content))

    def exit(self):
        self.socket.close()


if __name__ == '__main__':
    me = ChatClient()
    me.run()
