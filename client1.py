import socket
import threading
import os
import time

ENCODER="utf-8"

HOST='localhost'
FILE_SHARE_PORT= 8000
GROUP_CHAT_PORT= 8001
PORT= 9000


def recieve_server(client_socket):
    try:
        while True:
            message=client_socket.recv(1024).decode()
            print(message)
    except :
        print("Server closed")

def GroupChat():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,GROUP_CHAT_PORT))
    nickname=''

    while True:
        message= client_socket.recv(1024).decode(ENCODER)
        print(message)
        if message ==  "Your nickname is set":
            break
        
        nickname=input("Write Your Nickname: \n")

        client_socket.send(nickname.encode(ENCODER))
    
    client_socket.send("online".encode(ENCODER))
    while True:
        message= client_socket.recv(1024).decode()
        if message == '<END>':
            #print("ber ho")
            break
        else:
            print(message)
    
    newthread=threading.Thread(target=recieve_server,args=(client_socket,))
    newthread.start()

    while True:
        message=input("[YOU]: Type...\n")
        # message=f"[{nickname}]: "+message
        client_socket.send(message.encode(ENCODER))
        if message=='quit':
            print("Leaving Chat...")
            break
    
    client_socket.close()
    newthread.join()

    return


    

def send(client, addr):
    path= "C:\\Users\\HP\\Documents\\Chatter_Share\\source"
    
    file_list= os.listdir(path)
    send=""
    if len(file_list)==0:
        send += "The server directory is empty"
    else:
        send += "\n".join(f for f in file_list)
    
    time.sleep(0.01)
    print("Sending file list")
    
    client.send(send.encode(ENCODER))

    # print(send)
    while True:

        file_name=client.recv(1024).decode(ENCODER)
        if file_name == 'quit':
            break
        else:
            file_name=path+"\\"+file_name
            try:
                file= open(file_name,"rb")
                file_size=os.path.getsize(file_name)
                print(file_size)
                client.send(f"{str(file_size)}".encode(ENCODER))

                st=time.time()
                data=file.read()
                client.sendall(data)
                client.send(b"<END>")

                file.close()
                stop=time.time()
                print("Finished")
                print("Elapsed:", stop-st)
                print(f"Disconnected with- {addr[0]} {addr[1]}")
                break
            except:
                client.send("ERROR File Not Found".encode(ENCODER))
                print("File Not found.")
                continue

    client.close()

def SendingThread(server_socket):
    try:
        while True:
            client,addr=server_socket.accept()
            
            print("Connected to :",addr[0],":",addr[1])
            t = threading.Thread(target=send, args=(client,addr))
            t.start()
    except Exception:
        print("Exception in client threading...")


def startRecieve(host,port):
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((host,port))
    print("Connected...")
    
    print("\nAvailable file list...")
    time.sleep(0.01)
    listed=client_socket.recv(1024).decode(ENCODER).split("\n")
    # print("hello")

    for lis in listed:
        print(lis)
    
    time.sleep(0.1)

    print("Write the file name that you want to recieve.\nPlease type carefully so that it matches the file name (Type 'quit' to quit)")
    f=0
    while True:
        file=input()
        client_socket.send(file.encode(ENCODER))
        if file == 'quit':
            client_socket.close()
            f=1
            break
        
        fl=client_socket.recv(1024).decode()
        path= "C:\\Users\\HP\\Documents\\Chatter_Share\\target"

        if fl=="ERROR File Not Found":
            print("File name Error...")
            print("Type again...")
            continue
        else :
            break

    if f==1:
        return
            
    file= open(path+"\\"+file,"wb")
    file_bytes=b""
    st=time.time()
    seq=0
    while True:
        message=client_socket.recv(1024)

        if file_bytes[-5:]==b"<END>":
            print("\nEnding...")
            break
        else:
            file_bytes+=message
            print(f"File recieved from {seq} byte")
            seq+=len(message)
    
    file.write(file_bytes[:-5])
    file.close()

    print("File Recieved Successfully...")
    print("Time Taken-",time.time()-st)


    client_socket.close()

    

def RecieveFile(client_socket):
    while True:
        client_socket.send("online".encode(ENCODER))
        while True:
            message= client_socket.recv(1024).decode()
            if message == '<END>':
                #print("ber ho")
                break
            else:
                print(message)

        print("Type The Nickname Of The Client From Whom You Want To Recieve\n")
        name=input()
        if name== 'quit':
            break
        else:
            client_socket.send(name.encode(ENCODER))
            message=client_socket.recv(1024).decode()
            message=message.split(":")
            host=message[0]
            port=message[1]
            port=int(port)
            print(f"{host}  {port}")
            startRecieve(host,port)



def FileShare():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,FILE_SHARE_PORT))

    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))

    server_socket.listen()

    print("Server is running...")

    sendThread=threading.Thread(target=SendingThread,args=(server_socket,))
    sendThread.start()

    while True:
        message= client_socket.recv(1024).decode(ENCODER)
        print(message)
        if message ==  "Your nickname is set":
            break
        
        nickname=input("Write Your Nickname: \n")

        client_socket.send(nickname.encode(ENCODER))

    # time.sleep(2)
    client_socket.send(str(PORT).encode(ENCODER))

    while True:
        print("What Do You Want To Do-\nType 1 To Recieve File\nType 'quit' to quit\n")
        x=input()

        if x=='1':
            RecieveFile(client_socket)
        elif x=='quit':
            print("Closing File Sharing")
            client_socket.send(x.encode(ENCODER))
            client_socket.close()
            break
        else:
            print("Invalid Response...Try again\n")

    
def main():
    print("What do you want to do?")
    while True:
        print()
        print("*****Type 1 for file sharing*****")
        print("*****Type 2 for group chat*****")
        print("(Type 'quit' to stop the program)\n")
        x=input()
        if x=='1':
            FileShare()
        elif x=='2':
            GroupChat()
        elif x=='quit':
            break
        else:
            print("Please type correctly...")
    print("\nBYE!")


if __name__=='__main__':
    main()