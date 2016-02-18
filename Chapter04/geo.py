import pygeoip

gi = pygeoip.GeoIP("GeoLiteCity.dat")


def printRecord(target):
    rec = gi.record_by_name(target)
    city = rec['city']
    region = rec['region_code']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print('[*] Target:', target, "Geo-located.")
    print("[+]", city + ", " + region + ", " + country)
    print('[+] Latitude:', lat, 'Longitude:', long)


if __name__ == '__main__':
    target = '168.255.226.98'
    printRecord(target)
