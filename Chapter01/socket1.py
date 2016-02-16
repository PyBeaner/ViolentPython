import socket
import sys
import os


def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        ans = s.recv(1024)
        return ans
    except Exception as e:
        print("[-] Error = ", e)


def checkBanner(banner, filename):
    if not banner:
        return
    for line in open(filename):
        if line.strip() in banner:
            print("[+] Server is vulnerable: ", banner)
            return


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = "vuln_banners.txt"
    if not os.path.isfile(filename):
        print("[-]", filename, "does not exist.")
        exit(0)
    if not os.access(filename, os.R_OK):
        print("[-]", filename, "access denied.")
        exit(0)
    port_list = [21, 22, 25, 80, 110, 443]
    for x in range(1, 255):
        ip = "192.168.1." + str(x)
        for port in port_list:
            banner = retBanner(ip, port)
            print("[+] Checking", ip + str(port), ": ", banner)
            checkBanner(banner, filename)
