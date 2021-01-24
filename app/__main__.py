import CloudFlare
import time
import datetime
import pytz
import json

from CFStats import CFStats
from CFProcess import CFProcess

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

    # Week of data.
    start_date = now_iso8601_time(0)[0:10]
    end_date = now_iso8601_time(30 * 24)[0:10]
    
    result = {}
    for zone in zones:
        res = cf.stats(
            zone['id'],
            start_date,
            end_date
        )
        result[zone['name']] = CFProcess(res).all()
        
        # Commented out, but if you are doing debugging and want a file saved
        # locally, here you go:
        #
        # f = open('samples/{}-{}_{}.json'.format(
        #           zone['id'], start_date, end_date), 'w')
        # f.write(data)
        # f.close()

    print(json.dumps(result))

if __name__ == "__main__":
    main()
