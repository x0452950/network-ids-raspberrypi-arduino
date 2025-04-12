import subprocess
import serial
import time

# Set of known, authorized IP addresses (can be edited)
authorized_ips = {
    '192.168.1.1',  # Router
    '192.168.1.100',  # Your PC
    '192.168.1.101',  # Your phone
}

# Arduino serial config
arduino_port = '/dev/ttyUSB0'  # Change if needed (e.g., COM3 on Windows)
baud_rate = 9600

def get_connected_ips():
    try:
        result = subprocess.check_output(['arp', '-a']).decode()
        ips = set()
        for line in result.split('\n'):
            if '(' in line and ')' in line:
                ip = line.split('(')[1].split(')')[0]
                ips.add(ip)
        return ips
    except Exception as e:
        print(f"[!] Error getting IPs: {e}")
        return set()

def send_alert():
    try:
        with serial.Serial(arduino_port, baud_rate, timeout=2) as arduino:
            time.sleep(2)
            arduino.write(b'ALERT\n')
            print("[+] Alert sent to Arduino.")
    except Exception as e:
        print(f"[!] Failed to send alert: {e}")

def main():
    print("[*] Scanning for unauthorized IPs...")
    connected_ips = get_connected_ips()
    unauthorized = connected_ips - authorized_ips
    if unauthorized:
        print("[!] Unauthorized device(s) detected:")
        for ip in unauthorized:
            print(f"  - {ip}")
        send_alert()
    else:
        print("[+] All devices are authorized.")

if __name__ == "__main__":
    main()
