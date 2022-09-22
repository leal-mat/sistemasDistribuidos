import socket
import json
import re

HOST = "127.0.0.1"
PORT = 6789


exp_str = input("Type a expression: ")

args_list = re.split(" +", exp_str, 2)

message_ok = False
try:

    exp = {
        "op": args_list[1],
        "n1": float(args_list[0]),
        "n2": float(args_list[2]),
    }
    message_ok = True
except:
    print("Algum argumento está invalido.")

if message_ok:

    exp_json = json.dumps(exp)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)

    try:
        s.sendto(bytes(exp_json, "utf-8"), (HOST, PORT))
        reply, address = s.recvfrom(1024)
        reply_json = json.loads(reply)
        print(reply_json["exp"] + " = " + str(reply_json["result"]))
        s.close()
    except:
        print("Tempo excedido")
