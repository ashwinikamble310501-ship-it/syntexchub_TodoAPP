import socket
import threading
from queue import Queue
import datetime

print_lock = threading.Lock()
open_ports = []

def scan_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))

        with print_lock:
            if result == 0:
                print(f"Port {port} - Open")
                open_ports.append(port)
            else:
                print(f"Port {port} - Closed")

        s.close()

    except socket.timeout:
        print(f"Port {port} - Timeout")
    except Exception as e:
        print(f"Error on port {port}: {e}")

def worker():
    while True:
        port = q.get()
        scan_port(target, port)
        q.task_done()

target = input("Enter Target IP or Host: ")
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter End Port: "))

q = Queue()

print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

for _ in range(50):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

for port in range(start_port, end_port + 1):
    q.put(port)

q.join()

# Save results to file
with open("scan_results.txt", "w") as f:
    f.write(f"Scan Date: {datetime.datetime.now()}\n")
    f.write(f"Target: {target}\n")
    f.write("Open Ports:\n")
    for port in open_ports:
        f.write(f"{port}\n")

print("\nScanning Completed ✅")
print("Results saved in scan_results.txt")
