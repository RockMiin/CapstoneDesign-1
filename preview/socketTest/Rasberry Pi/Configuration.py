import os
import sys


class Configuration:

    KEY_SERVER_IP = "SERVER_IP"
    KEY_SERVER_PORT = "SERVER_PORT"
    KEY_MOISTURE_IP = "MOISTURE_IP"
    KEY_LIGHT_IP = "LIGHT_IP"

    def __init__(self, config_path):
        self.SERVER_IP = None
        self.SERVER_PORT = None
        self.MOISTURE_IP = None
        self.LIGHT_IP = None

        self.set_config(config_path)
        self.print_info()

    def set_config(self, config_path):
        if os.path.exists(config_path) is False:
            print("[ERROR] Invalid configuration path")
            sys.exit(1)

        with open(config_path, 'r') as fd:
            lines = fd.readlines()

        self._parse(lines)

    def _parse(self, lines):
        for line in lines:
            line = line.strip()

            key = line.split('=')[0]
            value = line.split('=')[1]

            if key == Configuration.KEY_SERVER_IP:
                self.SERVER_IP = value
            elif key == Configuration.KEY_SERVER_PORT:
                self.SERVER_PORT = int(value)
            elif key == Configuration.KEY_MOISTURE_IP:
                self.MOISTURE_IP = value
            elif key == Configuration.KEY_LIGHT_IP:
                self.LIGHT_IP = value
            else:
                print("[ERROR] Invalid config key : " + line)

    def print_info(self):
        print("")
        print("------------------------------------")
        print("Configuration")
        print("      IP              : ", self.SERVER_IP)
        print("      PORT            : ", self.SERVER_PORT)
        print("      MOISTURE_IP     : ", self.MOISTURE_IP)
        print("      LIGHT_IP  : ", self.LIGHT_IP)

    def get_server_ip(self):
        return self.SERVER_IP

    def get_server_port(self):
        return self.SERVER_PORT

    def get_moisture_ip(self):
        return self.MOISTURE_IP

    def get_light_ip(self):
        return self.LIGHT_IP