#! /usr/bin/env python3

from requests import get

bgpstuff_url = 'https://bgpstuff.net/{}?{}&format=json'

def main():

    my_ip = get('http://ifconfig.me')
    print(my_ip.text)
    my_ip = f'ip={my_ip.text}'

    route = get(bgpstuff_url.format('route', my_ip)).json()
    print(route)
    origin = get(bgpstuff_url.format('origin', my_ip)).json()
    print(origin)
    aspath = get(bgpstuff_url.format('aspath', my_ip)).json()
    print(aspath)
    roa = get(bgpstuff_url.format('roa', my_ip)).json()
    print(roa)

    asn = f"as={origin['originAsn']}"
    asname = get(bgpstuff_url.format('asname', asn)).json()
    print(asname)
    sourced = get(bgpstuff_url.format('sourced', asn)).json()
    print(sourced)




if __name__ == '__main__':
    main()
