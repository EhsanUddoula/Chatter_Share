import socket
import threading
import os
import time

ENCODER="utf-8"

HOST='localhost'
PORT= 8001

clients=[]

def broadcast(message):
    for client in clients:
        client["address"].send(message.encode(ENCODER))

def threaded(c,addr):
    c.send("Give a nickname".encode(ENCODER))
    while True:
        recieved_nickname=c.recv(1024).decode(ENCODER)
        f=0
        for client in clients:
                if client["name"]==recieved_nickname:
                    c.send("Nickname already exists Or invalid,Please provide unique name-\n".encode(ENCODER))
                    f=1
                    break
        if f==1:
            continue

        if recieved_nickname=='quit':
            c.send("Nickname already exists Or invalid,Please provide unique name-\n".encode(ENCODER))
        else:
            c.send("Your nickname is set".encode(ENCODER))
            
            client_dic={"name": recieved_nickname, "address": c, "HOST": addr[0], "PORT": addr[1]}

            clients.append(client_dic)
            broadcast(f"{recieved_nickname} has joined the chat")
            break
    

    while True:
        message=c.recv(1024).decode(ENCODER)
        if message=='quit':
            for client in clients:
                if client["name"]==recieved_nickname:
                    clients.remove(client)
                    break
            broadcast(f"{recieved_nickname} has left the chat\n")
            c.close()
            print(f"Disconnect with {addr[0]} : {addr[1]}")
            break
        elif message == 'online':
            c.send("Online Now-\n".encode(ENCODER))
            for client in clients:
                c.send(f"{client["name"]}".encode(ENCODER))
                time.sleep(0.001)
            c.send("<END>".encode(ENCODER))
        else:
            message=f"[{recieved_nickname}]: "+message
            broadcast(message)

    


def main():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen()

    print("Server is running...")

    try:
        while True:
            client,addr=server_socket.accept()
            
            print("Connected to :",addr[0],":",addr[1])
            t = threading.Thread(target=threaded, args=(client,addr))
            t.start()
    except KeyboardInterrupt:
        print("Stopped by Ctrl+C")
    except Exception:
        client.close()
        print(f"Disconnect with {addr[0]} : {addr[1]}")
        
    server_socket.close()
    
if __name__ == '__main__':
    main()
