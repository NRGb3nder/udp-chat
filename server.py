import socket
import time
import os
import threading

class ChatServer(threading.Thread):
    UDP_CONFIG = ("localhost", 4000)
    MSG_HANDSHAKE = '/::handshake::/'
    MSG_SIZE = 512

    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(ChatServer.UDP_CONFIG)
        self.socket.setblocking(0)
        self.clients = []

    def run(self):
        os.system('clear')
        print('>> Server started\n>>')
        self.serve()

    def serve(self):
        while True:
            try:
                msg, addr = self.socket.recvfrom(ChatServer.MSG_SIZE)
                if addr not in self.clients:
                    self.clients.append(addr)
                msg = msg.decode('utf-8')
                if ChatServer.MSG_HANDSHAKE in msg:
                    msg = msg.replace(ChatServer.MSG_HANDSHAKE, '')
                    msg = 'User ' + msg + ' has logged in!'
                print(">> [{:02d}:{:02d}:{:02d}] {}".format(*(time.localtime()[3:6] + (msg,))))
                for client in self.clients:
                    if addr != client:
                        self.socket.sendto(msg.encode('utf-8'), client)
            except:
                pass

server = ChatServer()
server.start()
