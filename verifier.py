"""
Write code for your verifier here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
from validate import *
import pathlib

def validate_and_clean(records: dict) -> bool:
    for domain, ports in records.items():
        if len(ports) > 1:
            return False
        elif len(ports) == 1:
            # Update the domain's value with the single port number
            records[domain] = ports[0]
    return records
    
def read_master_file(filepath: str) -> dict[str, list[int]]:
    """Reads the master file and returns a dictionary with domain as key and a list of ports as value."""
    records = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()
        port = validate_port(lines[0].strip())
        if port is False: raise ValueError
        for line in lines[1:]:
            try:
                domain, port = line.strip().split(',')
            except:
                raise ValueError
            domain_valid = validate_domain(domain, True)
            port_valid = validate_port(port)
            if (domain_valid is False) or (port_valid is False): raise ValueError
            # Use a list to store multiple ports for a domain
            if domain not in records:
                records[domain] = []
            records[domain].append(port)
    return records

def read_single_file(filepath: str) -> dict[int, dict[str, int]]:
    config_records = {}
    subconfig_records = {}
    root_records = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()
        head_port = validate_port(lines[0].strip())
        if head_port is False: raise ValueError
        for line in lines[1:]:
            try:
                domain, port = line.strip().split(',')
            except:
                raise ValueError
            domain_valid = validate_domain(domain, False)
            port_valid = validate_port(port)
            if (domain_valid is False) or (port_valid is False): raise ValueError
            if len(domain.split(".")) == 1:
                # Use a list to store multiple ports for a domain
                if domain not in root_records:
                    root_records[domain] = []
                root_records[domain].append(port)
            else:
                # Use a list to store multiple ports for a domain
                if domain not in subconfig_records:
                    subconfig_records[domain] = []
                subconfig_records[domain].append(port)
                config_records[head_port] = subconfig_records
    return root_records, config_records


def neq_checker(master_dict, root_dict, single_dict):
    
    for domain in master_dict.keys():
        parts = domain.split(".")
        root = parts[-1]
        tld = ".".join(parts[-2:])

        if root not in root_dict:
            return False
        root_port = root_dict[root]

        if root_port not in single_dict:
            return False
        config_dict = single_dict[root_port]

        if tld not in config_dict:
            return False
        tld_port = config_dict[tld]

        if tld_port not in single_dict:
            return False
        config_dict = single_dict[tld_port]

        if domain not in config_dict:
            return False
        domain_single_port = config_dict[domain]

        if domain not in master_dict or master_dict[domain] != domain_single_port:
            return False

    return True

def main(args: list[str]) -> None:
    if len(args) != 2:
        print("invalid arguments")
        exit()

    master_file_path = pathlib.Path(args[0])
    single_files_directory = pathlib.Path(args[1])

    master_data = {}
    root_data = {}
    config_data = {}

    try:
        master_data = read_master_file(master_file_path)
    except:
        print("invalid master")
        quit()

    if not single_files_directory.is_dir():
        print("singles io error")
        exit()

    for single_file in single_files_directory.iterdir():
        single_file_path = single_file

        try:
            single_file_extract = read_single_file(single_file_path)
        except Exception as e:
            print("invalid single")
            exit()

        root_dict, config_dict = single_file_extract
        root_data.update(root_dict)
        config_data.update(config_dict)
    
    for key, sub_dict in config_data.items():
        cleaned_data = validate_and_clean(sub_dict)
        if not cleaned_data:
            print("neq")
            quit()
        config_data[key] = cleaned_data
    
    master_data = validate_and_clean(master_data)
    root_data = validate_and_clean(root_data)

    if not neq_checker(master_data, root_data, config_data):
        print("neq")
        quit()
    
    print("eq")


if __name__ == "__main__":
    main(argv[1:])