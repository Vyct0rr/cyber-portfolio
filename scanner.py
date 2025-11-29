# Project: Basic Port Scanner (Verbose Mode)
# Author: Vyct0rr
# Description: Checks ports and prints status for EVERY attempt.

import socket
import sys
from datetime import datetime

# 1. Ask the user for the target
target = input("Enter the IP address to scan (e.g., 127.0.0.1): ")

# 2. Translate hostname to IP
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()

# 3. Print a nice banner
print("-" * 50)
print(f"Scanning Target: {target_ip}")
print(f"Time started: {datetime.now()}")
print("-" * 50)

# 4. The Scanning Loop
try:
    # We are scanning from port 7990 to 8005 to test your python server.
    # You can change this back to range(1, 85) later if you want.
    for port in range(7990, 8005): 
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5) # Wait 0.5 seconds max
        
        # Print "Checking..." without moving to a new line yet
        print(f"Checking Port {port}...", end=" ") 
        
        # Attempt to connect
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            print("OPEN! ✅") # Success message
        else:
            print("Closed")   # Failure message
        
        s.close() # Close connection

except KeyboardInterrupt:
    print("\nExiting Program.")
    sys.exit()

except socket.error:
    print("Could not connect to server.")
    sys.exit()

print("-" * 50)
print("Scan completed.")