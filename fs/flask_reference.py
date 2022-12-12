import os
import queue
import socket
import threading

import flask

from fs.constants import SOCKET_SERVER_PORT

app = flask.Flask(__name__)
q = queue.Queue()


def thread_info():
    return f"{os.getpid()}/{threading.current_thread().name}"


@app.route("/")
def index():
    msg = flask.request.args.get("msg", "")
    q.put_nowait(
        f"msg='{msg}' clientip={flask.request.remote_addr} query={thread_info()}"
    )
    form = '<form action="."><input name=msg type=text /><br/><input type=submit value="send" /></form>'
    return f'Forwarded "{msg}" forwarded {form}'


def worker_thread(parent_thread_info):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("localhost", SOCKET_SERVER_PORT))
        while True:
            item = q.get()
            msg = f"{__file__.rsplit('/', 1)[1]} {item} worker={thread_info()} main={parent_thread_info}"
            sock.sendall(msg.encode("ascii"))
            print(f">> background response {sock.recv(1024).decode()}")


def main():
    threading.Thread(target=worker_thread, args=(thread_info(),)).start()
    app.run("localhost", port=8000)


if __name__ == "__main__":
    main()
