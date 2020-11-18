# -*- coding: utf-8 -*-
# @Time    : 2020-11
# @Author  : PAO
# @File    : client.py
# @Software: PyCharm
from tkinter import Frame, Label, Entry, Button, Text, messagebox, Tk, Scrollbar, VERTICAL, END
import socket
import threading
import struct
import json


class client(object):
    """docstring for GUI"""
    client_socket = None
    last_received_message = None

    def __init__(self, ip, port):

        self.init_scoket(ip, port)  # call this method before starting GUI

    #       self.login1(username,password)
    #      self.showcommand()
    #    self.listen_mesg()
    def getcommand(self):
        # Instruction Set
        type = "IS"
        data = "getIS"
        self.send_mesg(data, type)
        buffer = self.client_socket.recv(1024)
        mesg = json.loads(buffer.decode("utf-8"))
        return mesg['data']

    # 展示命令操作指令
    def showcommand(self):
        return (self.getcommand())

    def getchatlist(self):
        # Instruction Set
        type = "chat"
        data = "getchatlist"
        self.send_mesg(data, type)
        buffer = self.client_socket.recv(1024)
        mesg = json.loads(buffer.decode("utf-8"))
        return mesg['data']

    # 展示用户在线列表
    def showchatlist(self):
        print(self.getchatlist())

    #
    # 初始化 Scoket
    def init_scoket(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        # 连接服务器
        self.client_socket.connect((remote_ip, remote_port))

    def login1(self, username, password):
        if (self.login(username, password)):
            print("Login successful")

        else:
            while (True):
                print("login false")
                command = input("reinput: R  exit: E")
                if (command == "R"):
                    username = input("Please input your username:")
                    password = input("Please input your password:")
                    self.login(username, password)
                elif (command == "E"):
                    exit()  # 暂时使用exit()暴力退出，后面需要写一个完整的退出函数
                else:
                    print("error input")

    def login(self, username, password):
        self.username = username
        self.send_mesg(password, "psw")
        mesg = self.client_socket.recv(1024)
        dirc = json.loads(mesg.decode('utf-8'))
        if dirc['data'] == "True":
            return True
        else:
            return False

    # listen_for_incoming_message_in_a_thread
    def listen_mesg(self):
        thread = threading.Thread(target=self.recv_mesg, args=(self.client_socket,))
        self.flag = 0
        thread.start()

    def thread_closed(self):
        self.flag = 1

    # receive_message_from_sever
    def recv_mesg(self, so):
        while True:
            if self.flag == 0:
                buffer = so.recv(1024)
                if not buffer:
                    break
                frame = json.loads(buffer.decode('utf-8'))
                print('\n' + frame['data'])
            else:
                break

    def send_mesg(self, data, type, toname='sever'):
        dirc = {
            'username': self.username,
            'type': type,
            'data': data,
            'toname': toname
        }
        packet = json.dumps(dirc)
        self.client_socket.send(packet.encode('utf-8'))
        print("send mesg: " + packet)

    def chat_close(self):
        data = "bye"
        type = "chat"
        self.send_mesg(data, type)

    def send_file(self, packet):
        print("send file" + packet)

    def close_so(self):
        print("close")


# now run our window here
if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 10319
    client1 = client(ip, port)
    username = input("Please input your username:")
    password = input("Please input your password:")
    while (True):
        if client1.login(username, password):
            print("Login successful")
            break
        else:
            print("login false")
            command = input("reinput: R  exit: E")
            if (command == "R"):
                username = input("Please input your username:")
                password = input("Please input your password:")
            else:
                exit()  # 暂时使用exit()暴力退出，后面需要写一个完整的退出函数
    command1 = input(client1.showcommand())
    if command1 == "mesg":
        client1.showchatlist()
        toname = input("while one do you want to chat ?\n>>")
        client1.listen_mesg()
        while True:
            tomesg = input(">>>>")
            # 这里需要一个退出机制
            if tomesg == "exit":  # 这里需要给服务器发一个再见的标志
                client1.chat_close()
                client1.thread_closed()
                break
            client1.send_mesg(tomesg, "mesg", toname)





