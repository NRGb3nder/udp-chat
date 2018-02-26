import socket
import time
import os
import threading

class ChatMessageReceiver(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.lock = threading.Lock()

    def run(self):
        while True:
            try:
                self.lock.acquire()
                while True:
                    msg = self.socket.recv(ChatClient.MSG_SIZE)
                    print("[{:02d}:{:02d}:{:02d}] {}".format(*(time.localtime()[3:6] +
                        (msg.decode('utf-8'),))), end='\n>> ')
            except:
                pass
            finally:
                self.lock.release()

class ChatMessageSender(threading.Thread):
    MSG_HANDSHAKE = '/::handshake::/'

    def __init__(self, socket, username):
        threading.Thread.__init__(self)
        self.socket = socket
        self.username = username

    def run(self):
        self.socket.sendto(bytes(ChatMessageSender.MSG_HANDSHAKE + self.username,
            'utf-8'), ChatClient.UDP_SERVER_CONFIG)
        while True:
            msg = self.username + ' says: ' + input('>> ')
            if (msg):
                self.socket.sendto(bytes(msg, 'utf-8'), ChatClient.UDP_SERVER_CONFIG)
                time.sleep(0.5)

class ChatClient(threading.Thread):
    UDP_HOST = "localhost"
    UDP_PORT = 1000
    UDP_SERVER_CONFIG = ("localhost", 4000)
    MSG_SIZE = 512
    MAX_BIND_TRIES = 1000

    def __init__(self):
        threading.Thread.__init__(self)
        os.system('clear')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind()
        self.socket.setblocking(0)

        print('>> Client started')
        self.username = input('>> Username: ')
        print('>>')

        self.receiver = ChatMessageReceiver(self.socket)
        self.sender = ChatMessageSender(self.socket, self.username)

    def run(self):
        self.receiver.start()
        self.sender.start()

    def bind(self):
        is_bind_success = False
        offset = 0
        while (offset < ChatClient.MAX_BIND_TRIES and not is_bind_success):
            try:
                self.socket.bind((ChatClient.UDP_HOST, ChatClient.UDP_PORT + offset))
                is_bind_success = True
            except:
                offset += 1

client = ChatClient()
client.start()
