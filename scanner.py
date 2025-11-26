# -----------------------------------------------------------
# Project: Basic Port Scanner
# Author: Victor Meseko (Vyct0rr)
# Description: Checks if common ports are open on a target.
# -----------------------------------------------------------

import socket # Import the library that lets us talk to the network
import sys    # Import library to handle system commands
from datetime import datetime # Import library to track time

# 1. Ask the user for the target to scan
target = input("Enter the IP address or website to scan (e.g., google.com): ")

# 2. Translate hostname to IP (e.g., google.com -> 142.250.x.x)
target_ip = socket.gethostbyname(target)

# 3. Print a nice banner
print("-" * 50)
print(f"Scanning Target: {target_ip}")
print(f"Time started: {datetime.now()}")
print("-" * 50)

# 4. The Scanning Loop
try:
    # We will scan ports 1 to 85 (the most common ports)
    for port in range(1, 85): 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1) # Wait 1 second max for a response
        
        # Attempt to connect to the port
        result = s.connect_ex((target_ip, port))
        
        # If result is 0, the port is OPEN
        if result == 0:
            print(f"Port {port}: OPEN")
        
        s.close() # Close connection and move to the next

except KeyboardInterrupt:
    print("\nExiting Program.")
    sys.exit()

except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()

except socket.error:
    print("Could not connect to server.")
    sys.exit()

print("-" * 50)
print("Scan completed!")