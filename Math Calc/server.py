import socket
import json
from expression import Expression

i = 0
HOST = ""
PORT = 6789
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
while True:
    i += 1

    print("Waiting...")
    request, address = sock.recvfrom(1024)
    print("Starting to calculate...")
    h, p = address

    request_json = json.loads(request.decode("utf-8"))
    exp = Expression(**request_json)
    reply = exp.calc()

    print("Calculation done...")

    reply_json = json.dumps(
        {
            "exp": str(request_json["n1"])
            + " "
            + request_json["op"]
            + " "
            + str(request_json["n2"]),
            "result": reply,
        }
    )
    sock.sendto(bytes(reply_json, "utf-8"), (h, p))
    print("Response sent to destinatary!")
