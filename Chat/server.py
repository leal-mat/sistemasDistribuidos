import socket
from threading import Thread
from utils import build_msg, new_connection, decode_msg
from threading import Lock

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 6789))
s.listen(1)

clients = dict()
all_messages = []

lock = Lock()

while True:
    conn, addr = s.accept()
    data_b = conn.recv(1024)
    data = decode_msg(data_b)

    notify = build_msg(True, "SERVER", data["user"] + " joined")

    with lock:
        for client in clients:
            clients[client]["conn"].sendall(notify)

        user_key = str(addr[0]) + ":" + str(addr[1])
        clients[user_key] = {"user": data["user"], "conn": conn}

    Thread(
        target=new_connection, args=(lock, conn, addr, clients, all_messages)
    ).start()
