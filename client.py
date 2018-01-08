import socket
SERVER_IP = ""
PORT = 0


class ChatClient(object):  
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((SERVER_IP, int(PORT)))
        self.run()

    def run(self):
        command = ""
        while "/exit" not in command:
            if "/send" in command[:5]:
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
