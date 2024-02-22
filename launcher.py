from sys import argv
from validate import *
import random
import pathlib

def read_master_file(filepath: str) -> dict[str, int]:
    """Reads the master file and returns a dictionary with domain as key and port as value."""
    records = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()
        port = validate_port(lines[0].strip())
        if port is False: print("INVALID MASTER"); quit()
        for line in lines[1:]:
            domain, port = line.strip().split(',')
            domain_valid = validate_domain(domain, True)
            port_valid = validate_port(port)
            if (domain_valid is False) or (port_valid is False): print("INVALID MASTER"); quit()
            records[domain.strip()] = int(port.strip())
    return records

def generate_single_files(master_records: dict[str, int], directory: str):
    """Generates the 'single' configuration files."""
    
    directory_path = pathlib.Path(directory)
    seen_root = set()
    seen_tld = set()

    # Dictionary to store the mapping between the domain and its port
    domain_to_port = {}

    # Save root domains to root.conf
    with (directory_path / "root.conf").open('w') as f:
        root_port = str(random.randint(1024, 65535))
        f.write(root_port + "\n")
        for domain, _ in master_records.items():
            parts = domain.split(".")
            root_domain = parts[-1]
            if root_domain in seen_root:
                continue
            seen_root.add(root_domain)
            port = str(random.randint(1024, 65535))
            domain_to_port[root_domain] = port
            f.write(f"{root_domain},{port}\n")

    # Group the master records by their parent domain (e.g. google.com)
    grouped_domains = {}
    for domain, port in master_records.items():
        parent_domain = ".".join(domain.split(".")[-2:])
        if parent_domain not in grouped_domains:
            grouped_domains[parent_domain] = {}
        grouped_domains[parent_domain][domain] = port

    # Save top-level domains to tld-(root).conf
    for root_domain, root_port in domain_to_port.items():
        with (directory_path / f"tld-{root_domain}.conf").open('w') as f:
            f.write(root_port + "\n")
            for parent_domain, records in grouped_domains.items():
                if parent_domain.endswith(root_domain) and parent_domain not in seen_tld:
                    seen_tld.add(parent_domain)
                    port_tld = str(random.randint(1024, 65535))
                    f.write(f"{parent_domain},{port_tld}\n")
                    with (directory_path / f"auth-{parent_domain.split('.')[0]}.conf").open('w') as auth_file:
                        auth_file.write(port_tld + "\n")
                        for domain, port in records.items():
                            auth_file.write(f"{domain},{port}\n")




def main(args: list[str]) -> None:
    if (len(args) != 2):
        print("INVALID ARGUMENTS")
        exit()

    master_file_path, single_files_dir = args

    if not pathlib.Path(master_file_path).exists():
        print("INVALID MASTER")
        exit()

    if not pathlib.Path(single_files_dir).exists():
        print("NON-WRITABLE SINGLE DIR")
        exit()

    master_records = read_master_file(master_file_path)
    generate_single_files(master_records, single_files_dir)

if __name__ == "__main__":
    
    main(argv[1:])
