import pxssh


def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print(s.before)


def connect(host, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        return s
    except Exception as e:
        print('[-] Error connecting')
        exit(0)


if __name__ == '__main__':
    s = connect('localhost', 'vagrant', 'vagrant')
    send_command(s, 'sudo cat /etc/shadow')
