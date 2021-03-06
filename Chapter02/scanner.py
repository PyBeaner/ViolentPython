import optparse
from socket import *
from threading import Thread, Semaphore

screenLock = Semaphore(value=1)


def connScan(host, port):
    conn = socket(AF_INET, SOCK_STREAM)
    try:
        conn.connect((host, port))
        conn.send("Hello")  # Anything
        resp = conn.recv(100)
        screenLock.acquire()
        print("[+] %d/tcp open" % port)
        print("[+]", resp)
    except Exception as e:
        screenLock.acquire()
        print("[-] %d/tcp closed" % port)
    finally:
        screenLock.release()
        conn.close()


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
        print("[+] Scan results for:", ip)

    for port in ports:
        # connScan(host, int(port))
        t = Thread(target=connScan, args=(host, int(port)))
        t.start()


def main():
    parser = optparse.OptionParser("usage%prog --host <target host> --ports <target port[s]>")
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
