import os
import socketserver
import threading

from fs.constants import SOCKET_SERVER_PORT


class EchoServer(socketserver.BaseRequestHandler):
    def handle(self):
        print(
            f"I am process:{os.getpid()} thread:{threading.current_thread().name}"
        )
        while True:
            data = self.request.recv(1024).strip()
            print(f"{self.client_address[0]}: {data.decode()}")
            self.request.sendall(b"OK")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    with ThreadedTCPServer(("localhost", SOCKET_SERVER_PORT), EchoServer) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
