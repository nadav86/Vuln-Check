import socket
import subprocess


# Function to check if a port is open
def is_port_open(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error as e:
        print(f"Error checking port {port} on {host}: {e}")
        return False


# Function to check if a port has a known vulnerability
def is_vulnerable(host, port):
    try:
        result = subprocess.run(["nmap", "-sV", "--script", "vuln", f"{host}:{port}"], capture_output=True, text=True)
        if "VULNERABLE" in result.stdout:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error running nmap on {host}:{port}: {e}")
        return False


# Main function to scan ports and check for vulnerabilities
def scan_ports(host):
    print(f"Scanning {host}...")
    for port in range(1, 1024):
        if is_port_open(host, port):
            if is_vulnerable(host, port):
                print(f"Port {port} is open and vulnerable on {host}")
            else:
                print(f"Port {port} is open on {host}")


# Get the IP address from user input
host1 = input("Enter the IP address to scan: ")

# Run the scan
scan_ports(host1)
