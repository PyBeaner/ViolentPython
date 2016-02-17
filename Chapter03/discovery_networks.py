from winreg import *
import requests
import json
import optparse


def wigleSession(username, password):
    session = requests.session()
    resp = session.request('post', 'https://wigle.net/api/v1/jsonLogin', data={
        'credential_0': username,
        'credential_1': password,
    })
    print(resp.content)
    resp_json = json.loads(resp.content.decode())
    if not resp_json['success']:
        print("Failed to login to wigle!", resp.content)
        return
    return session


def wiglePrint(session, netid):
    resp = session.request('post', 'https://wigle.net/api/v1/jsonSearch', {
        'netid': netid
    })
    print(resp.content)
    resp_json = json.loads(resp.content.decode())
    if not resp_json['success']:
        print("Failed to query info of MAC:", netid)
        return
        # TODO:parse the response


WIGLE_SESSION = None


def printNets():
    net = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    print("[*] Networks You have joined.")
    global WIGLE_SESSION
    for i in range(100):
        try:
            guid = EnumKey(key, i)
            netkey = OpenKey(key, str(guid))
            n, addr, t = EnumValue(netkey, 5)
            n, name, t = EnumValue(netkey, 4)
            mac = val2addr(addr)
            netName = str(name)
            print("[+]", netName, mac)
            wiglePrint(WIGLE_SESSION, mac)
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
    parser = optparse.OptionParser("usage%prog --u <user> -p <password>")
    parser.add_option("-u", dest='user', type='string')
    parser.add_option("-p", dest='password', type='string')
    options, args = parser.parse_args()
    user = options.user
    password = options.password
    if not (user and password):
        print(parser.usage)
        exit(0)
    WIGLE_SESSION = wigleSession(user, password)
    main()
