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

    # ftp.retrlines('RETR file', callback=None) # 读取文件内容
    # ftp.storlines('STOR file', callback=None) #　写入文件
    print(indexes(ftp))
