# -*- coding: utf-8 -*-
# @Time    : 2020-11
# @Author  : PAO
# @File    : server.py
# @Software: PyCharm
import socket
import threading
import struct
import json
import random
import string

class ChatServer:
    clients_list = []
    chatmember_list=[]
    last_received_message = ""

    def __init__(self,ip,port):
        self.server_socket = None
        self.create_server(ip,port)

    def create_server(self,ip,port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_ip = ip
        local_port = port
        # this is allow you ti immediately restart a TCP sever
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages...")
        self.server_socket.listen(5)
        self.receive_message_in_a_new_thread()

    def recv_mesg(self, so):
        while True:
            incoming_buffer = so.recv(1024)
            if not incoming_buffer:
                break
            self.last_received_message = json.loads(incoming_buffer.decode('utf-8'))
            #这里需要独立出来一个专门处理数据类型的函数
            type=self.last_received_message['type']
            if type=="psw":
                username=self.last_received_message['username']

                psw=self.last_received_message['data']
                if(self.check_psw(username,psw)==True):
                    #cookie=''.join(random.sample(string.ascii_letters + string.digits, 8))
                    dirc = {
                        'username': "Server",
                        #'cookie':cookie,
                        'type': type,
                        'data': "True"
                    }
                    packet = json.dumps(dirc)
                    so.sendall(packet.encode('utf-8'))
                    self.add_to_clients(so,username)
                else:
                    drc={
                        'username': "Server",
                        'type': type,
                        'data': "False"
                    }
                    packet = json.dumps(drc)
                    so.sendall(packet.encode('utf-8'))
            elif type=="IS":
                command=self.last_received_message['data']
                if command=="getIS":
                    dirc={
                        'username': "Server",
                        # 'cookie':cookie,
                        'type': type,
                        'data': "\t\tmesg: send mesg\n\t\tfile: send file\n------------------------\n>>"
                    }
                    packet = json.dumps(dirc)
                    so.sendall(packet.encode('utf-8'))
                else:
                    drc = {
                        'username': "Server",
                        'type': type,
                        'data': "error"
                    }
                    packet = json.dumps(drc)
                    so.sendall(packet.encode('utf-8'))
            elif type=="chat":
                command = self.last_received_message['data']
                if command == "getchatlist":
                    dirc = {
                        'username': "Server",
                        # 'cookie':cookie,
                        'type': type,
                        'data': str(self.chatmember_list)
                    }
                    packet = json.dumps(dirc)
                    so.sendall(packet.encode('utf-8'))
                elif command=="bye":
                    dirc = {
                        'username': "Server",
                        # 'cookie':cookie,
                        'type': type,
                        'data': "exit successful !"
                    }
                    packet = json.dumps(dirc)
                    so.sendall(packet.encode('utf-8'))
                else:
                    drc = {
                        'username': "Server",
                        'type': type,
                        'data': "error"
                    }
                    packet = json.dumps(drc)
                    so.sendall(packet.encode('utf-8'))
            elif type=='mesg':
                self.forword_mesg(self.last_received_message)
            print(self.last_received_message)
            #self.broadcast_to_all_clients(so)  # send to  all client
        so.close()
    def forword_mesg(self,packet):
        for (client1,username1) in self.clients_list:
            if username1==packet['toname']:
                client1.sendall((json.dumps(packet)).encode('utf-8'))

    def check_psw(self,username,psw):
        # 这里需要数据库来进行存储验证
        if psw=="wang":
            print("login successful")
            return True
        else:
            print("login defeat")
            return False


    def broadcast_to_all_clients(self, sender_sockets):
        for client in self.clients_list:
            print(client)
            (so,username) = client
           # if so is not sender_sockets:
            so.sendall(self.last_received_message.encode('utf-8'))

    def receive_message_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
           # self.add_to_clients(client)

            print('Connected to ',ip,':',str(port))

            t = threading.Thread(target=self.recv_mesg, args=(so,))
            t.start()

    def add_to_clients(self, client,username):
        if client not in self.clients_list:
            self.clients_list.append((client,username))
            self.chatmember_list.append(username)


if __name__ == "__main__":
    ip='127.0.0.1'
    port=10319
    ChatServer(ip,port)
