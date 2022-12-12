import os
import threading
import socket

import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from starlette.requests import Request

from fs.constants import SOCKET_SERVER_PORT

app = FastAPI()

socket_fd = None


def get_cached_per_process_socket() -> socket.socket:
    global socket_fd
    if socket_fd is None:
        print("connection")
        socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_fd.connect(("localhost", SOCKET_SERVER_PORT))
    return socket_fd


def thread_info():
    return f"{os.getpid()}/{threading.current_thread().name}"


@app.get("/")
async def index(
    request: Request,
    msg: str = "",
    s: socket.socket = Depends(get_cached_per_process_socket),
):
    content = f"{__file__.rsplit('/', 1)[1]} msg='{msg}' clientip={request.client.host} query={thread_info()}"
    s.sendall(content.encode("ascii"))
    print(f">> response {s.recv(1024).decode()}")
    return {"message": f"msg {msg} sent"}


if __name__ == "__main__":
    uvicorn.run("fastapi_bg:app", host="0.0.0.0", port=8003, workers=2)
