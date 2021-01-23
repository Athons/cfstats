import CloudFlare
import time
import datetime
import pytz
import json

from CFStats import CFStats
import settings

def now_iso8601_time(h_delta):
    """
    Taken from the CF examples, util for how they like their dates.
    """

    t = time.time() - (h_delta * 3600)
    r = datetime.datetime.fromtimestamp(int(t), tz=pytz.timezone("UTC")).strftime('%Y-%m-%dT%H:%M:%SZ')
    return r

def main():
    cf = CFStats(settings.token)
    zones = cf.zones()

    start_date = now_iso8601_time(0)[0:10]
    end_date = now_iso8601_time(7 * 24)[0:10]
    
    data = []
    for zone in zones:
        res = cf.stats(
            zone['id'],
            start_date,
            end_date
        )
        data = json.dumps(res)
        f = open('samples/{}-{}_{}.json'.format(
            zone['id'],
            start_date,
            end_date), 'w')
        f.write(data)
        f.close()

if __name__ == "__main__":
    main()
