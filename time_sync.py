"""Time sync helper using NTP (ntplib).
This module checks system clock offset against NTP servers and prints diagnostics.
It does NOT change system time automatically; run with privileges if you want to set system clock.
"""
import ntplib, time

def check_offset(servers=['pool.ntp.org']):
    client = ntplib.NTPClient()
    results = []
    for s in servers:
        try:
            r = client.request(s, version=3)
            offset = r.offset
            results.append((s, offset))
        except Exception as e:
            results.append((s, None))
    return results

if __name__=='__main__':
    import json
    servers = ['pool.ntp.org']
    res = check_offset(servers)
    print('NTP offsets:')
    print(json.dumps(res, indent=2))
