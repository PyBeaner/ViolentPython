import pexpect

PROMPTS = ["# ", ">>> ", "> ", "\$ "]


def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPTS)
    print(child.before)


def connect(host, user, password):
    ssh_newkey = "Are you sure you want to continue connecting"
    connStr = 'ssh ' + user + "@" + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print('[-] Error connecting')
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print('[-] Error connecting')
            return
    child.sendline(password)
    child.expect(PROMPTS)
    return child


def main():
    host = 'localhost'
    user = 'vagrant'
    password = 'vagrant'
    child = connect(host, user, password)
    if child:
        send_command(child, 'sudo cat /etc/shadow')


if __name__ == '__main__':
    main()
