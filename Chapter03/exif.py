import os
from urllib.parse import parse_qs
from urllib.request import urlparse

from PIL import Image
from PIL.ExifTags import TAGS
from bs4 import BeautifulSoup
import requests


def findImages(url):
    resp = requests.request('get', url)
    bs = BeautifulSoup(resp.content)
    imgs = bs.findAll('img')
    return imgs


def downloadImg(img):
    try:
        src = img.attrs['src']
        if not src.startswith("http"):
            print("Ignore img:", src)
            return
        print("Downloading image...:", src)
        resp = requests.request('get', src)
        o = urlparse(src)
        query = parse_qs(o.query)
        save_as = query.get("id")
        if save_as:
            save_as = save_as[0]
        else:
            save_as = os.path.basename(src)
        save_as = "/tmp/" + save_as
        f = open(save_as, 'wb')
        f.write(resp.content)
        return save_as
    except Exception as e:
        print(e)
        pass


def exif(file):
    data = {}
    f = Image.open(file)
    info = f._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            data[decoded] = value
        gps = data['GPSInfo']
        if gps:
            print("[*]", file, 'contains GPS Metadata:', gps)


if __name__ == '__main__':
    imgs = findImages("https://www.flickr.com/photos/dvids/4999001925/sizes/o")
    for img in imgs:
        save_as = downloadImg(img)
        if save_as:
            exif(save_as)
