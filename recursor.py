from sys import argv
from validate import *
import socket
import time

class Recursor:
    def __init__(self, root_port, timeout):
        self.root_port = int(root_port)
        self.timeout = float(timeout)
        self.start_time = None

    def _validate_domain(self, domain):
        # A simple domain validation could involve checking if the domain contains dots
        # This can be expanded for stricter validations
        parts = domain.split(".")

        if (len(parts) < 3):
            return False

        A = parts[-1]
        B = parts[-2]
        C = ".".join(parts[:-2])

        #Testing A and B

        if not A.isalnum() and '-' not in A:
            return False
        if not B.isalnum() and '-' not in B:
            return False
        
        #Testing C
        if C.startswith('.') or C.endswith('.'):
            return False
        for char in C:
            if not char.isalnum() and char not in '-.':
                return False
        
        return True
    
    def validate_port(x):
        if x.isdigit():
            return int(x)
        else:
            return False

    def _query_server(self, domain, port):
        # Simple simulation of querying a server via TCP. In reality, this would involve more detailed DNS operations.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.settimeout(self.timeout) # Set the timeout for socket operations
                s.connect(('localhost', port))
                s.sendall(domain.encode())
                response = s.recv(1024).decode()
                s.close()
            except socket.timeout:
                return "NXDOMAIN\n"
        return response

    def resolve(self, domain):
        if not self._validate_domain(domain):
            return "INVALID\n"
        
        parts = domain.split(".")


        # Step 1: Query root server
        try:
            response = self._query_server(parts[-1] + "\n", self.root_port)
        except:
            print("FAILED TO CONNECT TO ROOT", flush=True)
            quit()
        
        # For simplicity, assume responses are port numbers
        response = response.strip()

        try:
            tld_port = int(response)
        except:
            return "NXDOMAIN\n"

        # Step 2: Query TLD server
        try:
            response = self._query_server(".".join(parts[-2:]) + "\n", tld_port)
            response = response.strip()
        except:
            print("FAILED TO CONNECT TO TLD", flush=True)
            quit()

        try:
            authoritative_port = int(response)
        except:
            return "NXDOMAIN\n"

        # Step 3: Query authoritative nameserver
        try:
            final_response = self._query_server(domain + "\n", authoritative_port)
        except:
            print("FAILED TO CONNECT TO AUTH", flush=True)
            quit()


        return final_response

    def run(self):
        while True:
            try:
                domain = input("")

                if domain == 'exit':
                    break
                
                self.start_time = time.time()

                # Check for timeout
                if time.time() - self.start_time > self.timeout:
                    print("NXDOMAIN\n")
                    continue

                result = self.resolve(domain)
                print(result, end = "")
            except EOFError:
                quit()

if __name__ == "__main__":

    if len(argv) != 3:
        print("INVALID ARGUMENTS")
        quit()

    try:
        ROOT_PORT = validate_port(argv[1])
        TIMEOUT = float(argv[2])
        if ROOT_PORT is False: raise ValueError
    except:
        print("INVALID ARGUMENTS")
        quit()

    recursor = Recursor(ROOT_PORT, TIMEOUT)
    recursor.run()