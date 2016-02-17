from winreg import *


def printNets():
    net = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    print("[*] Networks You have joined.")
    for i in range(100):
        try:
            guid = EnumKey(key, i)
            netkey = OpenKey(key, str(guid))
            n, addr, t = EnumValue(netkey, 5)
            n, name, t = EnumValue(netkey, 4)
            mac = val2addr(addr)
            netName = str(name)
            print("[+]", netName, mac)
            CloseKey(netkey)
        except Exception as e:
            print(e)
            break


def val2addr(val):
    """
    convert bytes of mac to str
    :param val:
    :return:
    """
    addr = ''
    for ch in val:
        addr += '%02x ' % ord(chr(ch))
    addr = addr.strip().replace(' ', ":")[0:17]
    return addr


def main():
    printNets()


if __name__ == '__main__':
    main()
