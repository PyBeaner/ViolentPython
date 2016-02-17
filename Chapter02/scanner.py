import optparse
from socket import *


def connScan(host, port):
    try:
        conn = socket(AF_INET, SOCK_STREAM)
        conn.connect((host, port))
        conn.send("Hello")  # Anything
        resp = conn.recv(100)
        print("[+] %d/tcp open" % port)
        print("[+]", resp)
        conn.close()
    except Exception as e:
        print("[-] %d/tcp closed" % port)


def portScan(host, ports):
    try:
        ip = gethostbyname(host)
    except Exception as e:
        print("[-] Cannot resolve '%s': Unknown host" % host)
        return
    setdefaulttimeout(1)
    try:
        host_info = gethostbyaddr(ip)  # host,alias,ips
        print("[+] Scan results for:", host_info[0])
    except Exception as e:
        print(e)
        print("[+] Scan results for:", ip)

    for port in ports:
        print("Scanning port", port)
        connScan(host, int(port))


def main():
    parser = optparse.OptionParser("usage%prog --host <target host> --port <target port>")
    parser.add_option("--host", dest='host', type='string', help='specific target host')
    parser.add_option("--ports", dest='ports', type='string', help='specific target port[s] separated by comma')
    options, args = parser.parse_args()
    host = options.host
    ports = options.ports
    ports = str(ports).split(",")
    if (host is None) | (not ports):
        print("[-] You must specify a target host and port[s]")
        exit(0)
    portScan(host, ports)


if __name__ == '__main__':
    main()
