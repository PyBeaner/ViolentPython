# encoding=utf8
import os
from winreg import *


def recycleDir(partition="C"):
    """
    get the recycle bin path
    :param partition:
    :return:
    """
    dirs = ['Recycler', "Recycled", "$Recycle.Bin"]
    for dir in dirs:
        path = partition + ":\\" + dir
        if os.path.isdir(path):
            return path


def sid2user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\" + sid)
        value, type = QueryValueEx(key, "ProfileImagePath")  # the profile path
        user = value.split("\\")[-1]  # username
        return user
    except Exception as e:
        print(e)
        return sid


def findRecycled(recycleBin):
    user_dirs = os.listdir(recycleBin)
    for sid in user_dirs:
        user = sid2user(sid)
        print("[*] Listing files for user:", user)
        user_recycle_bin = os.path.join(recycleBin, sid)  # the recycle bin for the user
        files = os.listdir(user_recycle_bin)
        for file in files:
            fullname = os.path.join(user_recycle_bin, file)
            print("[+] Found file:", file, "Size:", os.path.getsize(fullname))


if __name__ == '__main__':
    recycleBin = recycleDir()
    findRecycled(recycleBin)
