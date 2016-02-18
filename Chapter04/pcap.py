import socket
from dpkt.ethernet import Ethernet
from dpkt.pcap import Reader


def printPcap(pcap):
    for ts, buf in pcap:
        try:
            eth = Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print("[+] Src:", src, "--> Dst:", dst)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    f = open("geotest.pcap")
    pcap = Reader(f)
    printPcap(pcap)
