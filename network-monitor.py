import platform    # Used to detect if we are on Windows or Linux
import subprocess  # Used to run the 'ping' command in the system terminal
import smtplib     # Used to send emails via SMTP protocol
import time        # Used for sleep delays between checks
import logging     # Used to create a log file of events
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ==========================================
# CONFIGURATION SECTION (EDIT THESE VALUES)
# ==========================================

# List of IP addresses or Hostnames to monitor
MONITORED_HOSTS = [
    "8.8.8.8",        # Google DNS (Example)
    "192.168.1.1",    # Local Router (Example)
    "example.com"     # Web Domain (Example)
]

# Email Configuration
# NOTE: For Gmail, you must use an 'App Password', not your login password.
# Enable 2FA on Google, then go to Account > Security > App Passwords.
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "mesekooluwajuwon@gmail.com"
SENDER_PASSWORD = "jgkpgskxjitvxzjr"
RECEIVER_EMAIL = "mesekooluwajuwon@gmail.com"

# How often to check the hosts (in seconds)
CHECK_INTERVAL = 60 

# ==========================================
# SETUP LOGGING
# ==========================================
# This creates a file named 'monitor.log' to record history
logging.basicConfig(
    filename='monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_ping_command(host):
    """
    Determines the correct ping command based on the Operating System.
    Windows uses '-n', Linux/Mac uses '-c' for the count flag.
    """
    system_os = platform.system().lower()
    if system_os == "windows":
        # -n 1: Send 1 packet, -w 1000: Wait 1000ms (1s) for timeout
        return ['ping', '-n', '1', '-w', '1000', host]
    else:
        # -c 1: Send 1 packet, -W 1: Wait 1 second for timeout
        return ['ping', '-c', '1', '-W', '1', host]

def is_host_online(host):
    """
    Pings the host to check connectivity.
    Returns True if Online, False if Offline.
    """
    command = get_ping_command(host)
    try:
        # subprocess.call returns 0 if successful (online), non-zero if failed
        # stdout=subprocess.DEVNULL hides the output from the console
        response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return response == 0
    except Exception as e:
        logging.error(f"Error checking host {host}: {e}")
        return False

def send_email_alert(host, status, previous_status):
    """
    Sends an email to the administrator when a status change is detected.
    """
    subject = f"Network Alert: {host} is {status.upper()}"
    
    body = f"""
    NETWORK STATUS CHANGE DETECTED
    ------------------------------
    Target Host: {host}
    New Status:  {status.upper()}
    Old Status:  {previous_status.upper()}
    Time:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Please investigate immediately.
    """

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        print(f"[*] Sending email alert for {host}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade the connection to secure encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        logging.info(f"Email alert sent for {host} ({status})")
        print("[*] Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        print(f"[!] Failed to send email: {e}")

def main():
    print("-------------------------------------------------")
    print(f"Network Monitor Started at {datetime.now()}")
    print(f"Monitoring {len(MONITORED_HOSTS)} hosts every {CHECK_INTERVAL} seconds.")
    print("Press Ctrl+C to stop.")
    print("-------------------------------------------------")

    # Dictionary to store the last known state of each host
    # Format: {'192.168.1.1': 'online', '8.8.8.8': 'offline'}
    host_states = {}

    # Initialize states (First run assumes everything is unknown, so we check first)
    for host in MONITORED_HOSTS:
        host_states[host] = "unknown"

    try:
        while True:
            for host in MONITORED_HOSTS:
                is_online = is_host_online(host)
                current_status = "online" if is_online else "offline"
                previous_status = host_states[host]

                # Check if status has changed
                if previous_status != "unknown" and current_status != previous_status:
                    # Log the change
                    log_msg = f"Status Change: {host} went from {previous_status} to {current_status}"
                    logging.warning(log_msg)
                    print(f"\n[!] {log_msg}")
                    
                    # Send Email
                    send_email_alert(host, current_status, previous_status)

                elif previous_status == "unknown":
                    # First run initialization
                    print(f"[*] Initial check: {host} is {current_status}")
                    logging.info(f"Initial check: {host} is {current_status}")

                # Update the state tracker
                host_states[host] = current_status

            # --- NEW ADDITION IS HERE ---
            # Print a message so the user knows the script is alive and waiting
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Scan cycle complete. Waiting {CHECK_INTERVAL}s...")
            
            # Wait before the next scan cycle
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping Network Monitor...")
        logging.info("Network Monitor stopped by user.")

if __name__ == "__main__":
    main()