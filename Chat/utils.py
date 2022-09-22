import json
from threading import Lock


def print_msg(msg):

    print()
    print("User:  ", msg["user"])
    print(">> ", msg["msg"])


def build_msg(connected, user, msg):
    cone = "1" if connected else "0"
    msg = {"connected": cone, "user": user, "msg": msg}
    return bytes(json.dumps(msg), "utf-8")


def decode_msg(msg):
    data = msg.decode("utf-8")
    if not data:
        return None
    return json.loads(data)


def build_user_list(user, clients):
    connected_users = "CONNECTED USERS:\n"
    for client in clients:
        connected_users += "\n" + clients[client]["user"]

    return build_msg(True, user, connected_users)


def new_connection(lock, conn, addrs, clients):

    addr_key = str(addrs[0]) + ":" + str(addrs[1])
    connected = True
    conn.sendall(build_msg(connected, "SERVER", ""))

    while connected:

        try:
            data_b = conn.recv(1024)

        except:
            connected = False
            clients.pop(addr_key)
            continue

        data = decode_msg(data_b)

        if data == None or data["connected"] == "0":
            connected = False
            conn.close()
            continue

        if data["msg"] == "/USUARIOS":
            conn.sendall(build_user_list("SERVER", clients))
            continue

        if data["msg"] == "/SAIR":
            conn.sendall(build_msg(False, "SERVER", "Desconectado com sucesso!"))
            with lock:
                user = clients.pop(addr_key)
                ntfy = f'Usuario Desconectado: {user["user"]}'
                for client in clients:
                    clients[client]["conn"].sendall(build_msg(True, "SERVER", ntfy))
            continue

        with lock:
            for client in clients:
                if addr_key != client:
                    clients[client]["conn"].sendall(data_b)


def waiting_messages(conn, connected):

    while connected:
        msg = conn.recv(1024)
        msg_decoded = decode_msg(msg)
        if msg_decoded["connected"] == "0":
            print("Desconectado com sucesso, aperte enter!")
            conn.sendall(build_msg(False, "SERVER", ""))
            conn.close()
            break

        print_msg(msg_decoded)
