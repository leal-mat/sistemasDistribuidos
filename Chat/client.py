from threading import Thread
from utils import build_msg, waiting_messages, decode_msg
import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False
user = ""
print("----------------------------")
print(
    """
      COMANDOS
      /ENTRAR ip:porta nickname\n
      /USUARIOS, para listar usuários \n
      /SAIR, para sair do chat\n
      """
)
print("----------------------------")
while not connected:

    msg = input()

    try:
        args_list = re.split("[ +]", msg, 2)
        addrs = args_list[1].split(":")
        user = args_list[2]
    except:
        print("Some argument is invalid! Try again")
        continue

    if args_list[0] == "/ENTRAR":
        try:
            s.connect((addrs[0], int(addrs[1])))
        except:
            print("Connection failed! Try again")
            continue

        s.sendall(build_msg(True, user, ""))
        ack = s.recv(1024)
        ack_decoded = decode_msg(ack)
        if ack_decoded != None:
            connected = True if ack_decoded["connected"] == "1" else False
            lobby = Thread(target=waiting_messages, args=(s, connected))
            lobby.start()

print("Conectado! \n")
while connected:
    msg = input()
    print("\033[1A" + "\033[K", end="")
    print(f"\nVocê >>>> {msg}")

    try:
        s.sendall(build_msg(connected, user, msg))
    except:
        print("\033[1A" + "\033[K", end="")
        s.close()
        break
