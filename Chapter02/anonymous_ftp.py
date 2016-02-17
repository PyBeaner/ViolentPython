import ftplib


def anonymous_login(host):
    try:
        ftp = ftplib.FTP(host)
        ftp.login('anonymous', 'hello@python.com')
        print('[*]', host, 'FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    except Exception as e:
        print('[-]', host, 'FTP Anonymous Logon Failed.', e)


if __name__ == '__main__':
    host = 'ftp.sjtu.edu.cn'
    print(anonymous_login(host))
