import nmap
import optparse


def nmapScan(host, port):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    state = scanner[scanner.all_hosts()[0]]['tcp'][int(port)]['state']
    print("[*]", host, "tcp/" + port, state)


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
    for port in ports:
        nmapScan(host, port)


if __name__ == '__main__':
    main()
