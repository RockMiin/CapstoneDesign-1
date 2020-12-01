import sys

from socket import *
from Configuration import Configuration
from concurrent.futures import ThreadPoolExecutor
from WriteSensorValue import WriteSensorValue


class RaspberryServer:

    def __init__(self, config_path):
        self.SERVER_CONFIG = Configuration(config_path)

        self.sock = None
        self.BUFSIZE = 1024
        self.classifying_pool = ThreadPoolExecutor(5)

        self._initialize_server()
        self.writer = WriteSensorValue()

    def _initialize_server(self):
        IP = self.SERVER_CONFIG.get_server_ip()
        PORT = self.SERVER_CONFIG.get_server_port()

        SERVER_ADDR = (IP, PORT)

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(SERVER_ADDR)

    def start(self):
        if self.sock is None:
            print("[ERROR] The socket has not been initialized")
            sys.exit(1)

        self.sock.listen(20)

        try:
            while True:
                client_socket, client_addr = self.sock.accept()
                print("[DEBUG] The client is connected. Connected IP : {}".format(client_addr[0]))

                if client_addr[0] == self.SERVER_CONFIG.get_moisture_ip():
                    self.classifying_pool.submit(self._set_moisture_client, client_socket)
                elif client_addr[0] == self.SERVER_CONFIG.get_light_ip():
                    self.classifying_pool.submit(self._set_light_client, client_socket)
                else:
                    print("[ERROR] Unknown client")

        except Exception as e:
            print("[ERROR] ", e)
        finally:
            self.sock.close()

    def _set_moisture_client(self, sock):
        self.writer.set_moisture_client(sock)

    def _set_light_client(self, sock):
        self.writer.set_light_client(sock)


if __name__ == '__main__':
    server = RaspberryServer('config/server.config')
    server.start()