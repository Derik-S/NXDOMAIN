from sys import argv
from validate import *
import pathlib
import socket


class Server:
    def __init__(self, config_file):
        self.config_file = config_file
        self.records = {}
        self.temp_records = {}
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                lines = file.readlines()
                port_validation_result = validate_port(lines[0].strip())
                if not port_validation_result:
                    raise ValueError
                self.port = int(port_validation_result)
                for line in lines[1:]:
                    domain, port_id = line.strip().split(',')
                    if not validate_domain(domain, False):
                        raise ValueError
                    self.records[domain] = port_id
        except:
            print("INVALID CONFIGURATION")
            exit()

    
    def add_hostname(self, record = {}):
        try:
            with open(self.config_file, "a") as file:
                for hostname, port in record.items():
                    file.write(f"{hostname}, {port}\n")
        except Exception as e:
            print(f"ERROR: {e}")
        return None

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode("utf-8")
        request = request.strip()
        if request.startswith('!'):
            # Handle commands
            if request.startswith('!ADD'):
                _, hostname, port = request.split()
                if hostname in self.records:
                    self.records[hostname] = port
                else:
                    self.temp_records[hostname] = port
                client_socket.send("".encode())
            elif request.startswith('!DEL'):
                _, hostname = request.split()
                if hostname in self.records:
                    del self.records[hostname]
                else:
                    client_socket.send("INVALID\n".encode())
                client_socket.send("".encode())
            elif request.startswith('!EXIT'):
                self.add_hostname()
                client_socket.close()
                exit(0)
            else:
                client_socket.send("INVALID\n".encode())
        else:
            # Resolve the domain name
            if (request in self.records):
                print(f"resolve {request} to {self.records[request]}", flush = True)
                response = f"{self.records[request]}\n"
            elif (request in self.temp_records):
                print(f"resolve {request} to {self.temp_records[request]}", flush = True)
                response = f"{self.temp_records[request]}\n"
            else:
                print(f"resolve {request} to NXDOMAIN", flush = True)
                response = "NXDOMAIN\n"
            client_socket.send(response.encode())

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', self.port))
        server.listen(5)
        
        while True:
            client, addr = server.accept()
            self.handle_client(client)

if __name__ == "__main__":

    if len(argv) != 2:
        print("INVALID ARGUMENTS")
        exit()
    
    config_file = argv[1]

    if not pathlib.Path(config_file).exists():
        print("INVALID CONFIGURATION")
        exit()
        
    server = Server(config_file)
    server.start()