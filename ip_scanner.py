# CODE DONE WITH NO VIBE CODING!!

import subprocess
from multiprocessing import Pool
import ipaddress
import platform
import time
import argparse
import json
import socket

# --PING SCANNING FUNCTION--------------------------------------------------------------------------

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

# --IP SCAN FUNCTION (WORKER)--------------------------------------------------------------------------

def ip_scan(result):
    answer_time = time.time()
    status_quo = permission(result)
    answer_time_end = time.time()
    answer_time_total = answer_time_end - answer_time
    answer_time_total = round(answer_time_total, 4)
    return (result,status_quo, answer_time_total)

print("Example in a IP address: 100.10.10")
print("Ranges in an IP direction are from 1 to 254")

# --PORT SCANNER--------------------------------------------------------------------------

def port_scan(ip):
    full_scan = subprocess.run()

# --FULL SCAN SUBNET FUNCTION (STILL EXPERIMENTAL)--------------------------------------------------------------------------

def subnet_full_scan(ip_network):
    global full_scan
    operating_sys = platform.system()
    if operating_sys == 'Linux':
        full_scan = subprocess.run(
        ["ping","-c", "1", "-W", "1", ip_network],
        stdout = subprocess.DEVNULL
        )
    return full_scan.returncode == 0

# --ARGUMENT PARSER SEGMENT--------------------------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--input",
    required = True,
    help="Enter the first three parts of the IP (e.g., 192.168.1) without line breaks"
)
parser.add_argument(
    "-r",
    "--range",
    required = True,
    type = int,
    help = "define the range by inputting a value between 1-254"
)

args = parser.parse_args()

# --IP DIRECTION AND RANGE SEGMENT--------------------------------------------------------------------------

base_input = args.input
ip_range = args.range

if args.input:
    test_ip = f"{base_input}.1"

    try:
        ipaddress.ip_address(test_ip)
        print(f"Base network '{base_input}' accepted.")
    except ValueError:
        print("Invalid format! Please use the correct IP format.")
        exit()

if args.range:
    try:

        if 1 <= ip_range <= 254:
            print("Ip range is valid!")

    except ValueError:
        print(f"Error! IP range exceeds 254 or is lower than 1. Try again.")
        print("Invalid format! Please use the 'X.X.X' format (0-255).")
        exit()

print(f"Your input '{ip_range}' was accepted.")

# --MULTIPROCESSING SEGMENT--------------------------------------------------------------------------
data = []

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

                data.append({"ip": result, "status": status_quo,"time": answer_time_total})

    endtime = time.time()
    print(f"Total time taken: {endtime - start_time} seconds.")

# --JSON DATAFILE SAVING--------------------------------------------------------------------------

    with open("ip_answers.json", "w") as outfile:
        json.dump(data, outfile)


# Upgrades:
# Detect mask automatically (low priority)
# sub red full scan with ipaddress.ip_network()
# Usage of "socket" library just to create a tool more precise
