import socket
import select
from server_info import ServerInfo
from client_handler.client_thread import ClientThread
from logger import Logger

class ServerMainLoop:
    def __init__(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.read_fds = set([self.listener])


    def exec(self):
        try:
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener.bind((ServerInfo.hostname, ServerInfo.port))
            self.listener.listen(ServerInfo.backlog)

        except BaseException as error:
            Logger.log("Server setup error: " + error.strerror)
            Logger.log("exiting...")

        else:
            while True:
                self.main_loop()

        finally:
            for sock in self.read_fds:
                sock.close()


    def main_loop(self):
        read_ready, write_ready, err_ready = select.select(self.read_fds, [], [])

        for sock in read_ready:
            if sock is self.listener:
                self.accept_new_client(sock)
            else:
                self.accept_new_message(sock)


    def accept_new_client(self, sock):
        conn, address = self.listener.accept()
        self.read_fds.add(conn)
        Logger.log("new client connected")


    def accept_new_message(self, sock):
        thread = ClientThread(sock)
        self.read_fds.remove(sock)
        thread.start()
