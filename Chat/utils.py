import json
import socket
from threading import Lock
from time import sleep


def print_msg(msg):

    print("___________________")
    print("User:  ", msg["user"])
    print(">> ", msg["msg"])
    print("___________________")


def build_msg(connected, user, msg):
    cone = "1" if connected else "0" 
    msg = {"connected": cone, "user": user, "msg": msg}

    return bytes(json.dumps(msg), "utf-8")

def decode_msg(msg):

    data = msg.decode("utf-8")

    if not data:
        return None
    # print(data)
    return json.loads(data)


def build_user_list(user, clients):
    connected_users = "CONNECTED USERS:\n\n"
    for client in clients:
        # print(clients[client]["user"])
        connected_users += clients[client]["user"] + "\n"

    return build_msg(True, user, connected_users)

def new_connection(lock, conn, addrs, clients, all_messages):

    addr_key = str(addrs[0]) + ":" + str(addrs[1])

    connected = True
    msg_s = build_msg(connected, "SERVER", "")
    conn.sendall(build_msg(connected, "SERVER", ""))

    while connected:

        data_b = conn.recv(1024)
        data = decode_msg(data_b)

        if data == None or data["connected"] == '0':
            connected = False
            conn.close()

        if (data["msg"] == "/USUARIOS"):
            conn.sendall(build_user_list("SERVER", clients))
            
            continue

        if (data["msg"] == "/SAIR"):
            conn.sendall(build_msg(False, "SERVER", "Desconectado com sucesso!"))
            clients.pop(addr_key)
            continue

        with lock:
            all_messages.append(data_b)
            for client in clients:
                if addr_key != client:
                    clients[client]["conn"].sendall(data_b)
                    print(data)


# def listing_users(lock, conn, addrs, clients):
#     connected = True
#     #msg = {"connected": connected, "user": user, "msg": msg}

#     while connected:

#         data_b = conn.recv(1024)
#         data = decode_msg(data_b)

#         if not data:
#             connected = False
#             conn.close()

#         with lock:
#             all_messages.append(data_b)

#             if addr_key != client:
#                 clients[client]["conn"].sendall(data_b)
#                 print(data)

#     return bytes(json.dumps(msg), "utf-8")


# def reading_old_messages(conn, reading):

#     msg = conn.recv(1024)
#     msg_decoded = decode_msg(msg)
#     print_msg(msg_decoded)
#     conn.sendall(bytes("0", "uftf-8"))


def waiting_messages(conn, connected):

    while connected:
        msg = conn.recv(1024)
        # print("msg: ", msg)
        msg_decoded = decode_msg(msg)
        # print("msg: ", msg_decoded)
        if msg_decoded["connected"] == "0":
            conn.sendall(build_msg(False, "SERVER", ""))
            print_msg(msg_decoded)
            conn.close()
            conn = None
            break
        
