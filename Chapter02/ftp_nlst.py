import ftplib


def indexes(ftp):
    try:
        dirList = ftp.nlst()  # list files under current/specific directory
    except Exception as e:
        dirList = []
        print('[-] Counld not list directory contents.')
        print('[-] Skipping To Next Target.')

    retList = []
    for filename in dirList:
        filename = filename.lower()
        if '.php' in filename or '.htm' in filename or '.asp' in filename:
            print("[+] Found default page:", filename)
            retList.append(filename)
    return retList


if __name__ == '__main__':
    host = 'ftp.cuhk.hk'
    user = 'anonymous'
    password = 'hello@python.org'
    ftp = ftplib.FTP(host)
    ftp.login(user, password)
    print(indexes(ftp))
