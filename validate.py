from sys import argv

def check_domains(domains):
    for port, domain in domains.items():
        if not validate_domain(domain, 1):
            raise ValueError
        if not validate_port(port):
            raise ValueError
        
def validate_port(port):
    try:
        port_int = int(port)
        if 1024 <= port_int <= 65535:
            return port
        else:
            return False
    except ValueError:
        return False


def validate_domain(domain, master):
    # A simple domain validation could involve checking if the domain contains dots
    # This can be expanded for stricter validations
    parts = domain.split(".")

    if master:
        if len(parts) < 3:
            return False
    
    A, B, C = None, None, None  # Initialize values to None
    if len(parts) == 0:
        return False
    if len(parts) >= 1:
        A = parts[-1]
    if len(parts) >= 2:
        B = parts[-2]
    if len(parts) >= 3:
        C = ".".join(parts[:-2])

    # Testing A
    if A and (not A.isalnum() and '-' not in A):
        return False

    # Testing B
    if B and (not B.isalnum() and '-' not in B):
        return False
    
    # Testing C
    if C:
        if C.startswith('.') or C.endswith('.'):
            return False
        for char in C:
            if not char.isalnum() and char not in '-.':
                return False
    
    return True