import subprocess
from multiprocessing import Pool
import ipaddress
import platform
import time

# ----------------------------------------------------------------------------

def permission(ip):
    operating_sys = platform.system()
    if operating_sys == 'Linux':
        answer = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL
        )
        return answer.returncode == 0
    elif operating_sys == 'Windows':
        host = ip
        command = ["ping", "-n", "1", host]
        answer = subprocess.run(command, capture_output=True, text=True)
        return answer.returncode == 0
    else:
        return False

# ----------------------------------------------------------------------------

def ip_scan(result):
    answer_time = time.time()
    status_quo = permission(result)
    answer_time_end = time.time()
    answer_time_total = answer_time_end - answer_time
    answer_time_total = round(answer_time_total, 4)
    return (result,status_quo, answer_time_total)

print("Example in a IP address: 100.10.10")
print("Ranges in an IP direction are from 1 to 254")

# ----------------------------------------------------------------------------

while True:
    base_input = input("Enter the first three parts of the IP (e.g., 192.168.1) without line breaks: ")

    test_ip = f"{base_input}.1"

    try:
        ipaddress.ip_address(test_ip)
        print(f"Base network '{base_input}' accepted.")
        break
    except ValueError:
        print("Invalid format! Please use the correct IP format.")

# ----------------------------------------------------------------------------

while True:
    try:
        ip_range = int(input("How many hosts do you want to scan (1-254)? "))

        if ip_range >= 1 and ip_range <= 254:
            print("Ip range is valid!")
            break
    except ValueError:
        print(f"Error! IP range exceeds 254 or is lower than 1. Try again.")
        print("Invalid format! Please use the 'X.X.X' format (0-255).")

print(f"Your input '{ip_range}' was accepted.")

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    ip_pool = []
    for i in range(1, ip_range + 1):
        ip = base_input + "." + str(i)
        ip_pool.append(ip)

    start_time = time.time()

    with Pool(10) as p:
        results = p.map(ip_scan, ip_pool)
        for result, status_quo, answer_time_total in results:
            if status_quo:
                print(f"Scanned IP {result} is responsive!")
                print(f"Total time taken: {answer_time_total} seconds.")

    endtime = time.time()
    print(f"Total time taken: {endtime - start_time} seconds.")


# ----------------------------------------------------------------------------

# Upgrades:
# Detect mask automatically (low priority)
# sub red full scan with ipaddress.ip_network()
# Usage of "socket" library just to create a tool more precise
# Integration of "argparse" for CLI usage instead of inputs
# JSON or TXT saving details
