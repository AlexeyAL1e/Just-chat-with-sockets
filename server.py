import socket
from threading import Thread


def broadcast(message):  # send messages to client
    for client in clients:
        client.send(message)


def get_message(client):
    while True:
        try:
            message = client.recv(2048)
            if len(nicknames) < 2:
                wait = "Please, wait to another users".encode('utf-8')
                broadcast(wait)
            else:
                broadcast(message)

        except ConnectionResetError:  # if client is close
            index = clients.index(client)
            nickname = nicknames[index]
            clients.remove(client)
            client.close()
            info = f"{nickname} <--- left the chat!"
            broadcast(info.encode('utf-8'))
            nicknames.remove(nickname)
            print(info, f"\nOnline users: {nicknames}")
            break


def connection():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        choose_name(client)

        thread = Thread(target=get_message, args=(client,))
        thread.start()


def choose_name(client):
    client.send("CHOOSE NAME".encode('utf-8'))  # send key word to client
    nickname = client.recv(1024).decode('utf-8')
    keyword = client.recv(1024).decode('utf-8')  # get key word

    nicknames.append(nickname)
    clients.append(client)

    if keyword == 'HELLO':
        send_hello(client, nickname)


def send_hello(client, nickname):  # at first connection
    message = f'{nickname} connected to the chat!'
    client.send("--Welcome to the chat!--".encode('utf-8'))

    print(message, f"\nOnline users: {nicknames}")

    for client in clients[:-1]:
        client.send(message.encode('utf-8'))


if __name__ == "__main__":
    while True:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("127.0.0.1", 1234))
            server.listen(20)  # max clients

            clients = []
            nicknames = []

            print("Server is listening...\n")
            connection()

        except ConnectionResetError:
            print("Connection Reset Error\n")

