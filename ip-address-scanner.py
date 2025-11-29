import socket

hostname = "google.com"

try:
    # This function resolves the name to an IPv4 address
    ip_address = socket.gethostbyname(hostname)
    print(f"The IP address of {hostname} is: {ip_address}")
except socket.gaierror:
    print("Hostname could not be resolved.")