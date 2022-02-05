import socket
from threading import Thread


def receive():
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message == "CHOOSE NAME":  # get key word from server
                client.send(nickname.encode('utf-8'))
                client.send("HELLO".encode('utf-8'))  # send key word to server

            else:
                print(message)

        except ConnectionAbortedError:
            print("An error occurred!")
            client.close()
            break


def send_message():
    while True:
        try:
            message = f"[{nickname}]: {input()}"
            client.send(message.encode('utf-8'))

        except UnicodeDecodeError:
            print("closing client!")
            client.close()


def start_client():
    receive_thread = Thread(target=receive)
    receive_thread.start()

    write_thread = Thread(target=send_message)
    write_thread.start()


if __name__ == "__main__":
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 1234))

        nickname = input("Connecting to the server... \nChoose your name: ")
        start_client()

    except ConnectionRefusedError:
        print("\nServer is offline!")

    except KeyboardInterrupt:
        print("\nAn error occurred!")



