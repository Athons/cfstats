import sys
import json

class CFProcess:
    """
    Takes a block of json from the requesting code and provides functions to
    handle what would be different graphs.
    """
    def __init__(self, data):
        self.data = sorted(data, key = lambda x: x['dimensions']['date'])

    def views(self):
        """
        Gets information on the page views, as reported by cloudflare.
        """
        return self._internal_read(
            lambda date, x: {
                'date': date,
                'pageViews': x['pageViews']
            }
        )

    def requests(self):
        return self._internal_read(
            lambda date, x: {
                'date': date,
                'requests': x['requests'],
                'cachedRequests': x['cachedRequests']
            }
        )

    def bytes(self):
        """
        Gets information on total bytes transfered.
        """
        return self._internal_read(
            lambda date, x: {
                'date': date,
                'bytes': x['bytes'],
                'cachedBytes': x['cachedBytes']
            }
        )

    def requests_ratio(self):
        return self._internal_read(
            lambda date, x: {
                'date': date,
                'requestRatio': float(x['cachedRequests']) / x['requests']
            }
        )



    def bytes_ratio(self):
        return self._internal_read(
            lambda date, x: {
                'date': date,
                'bytesRatio':  float(x['cachedBytes']) / x['bytes'],
            }
        )

    def _internal_read(self, f):
        """
        Keeping all these loops in one function to avoid code duplication
        """
        res = []
        for i in self.data:
            x = i['sum']
            date = i['dimensions']['date']
            res.append(
                f(date, x)
            )
        return res
    
    def all(self):
        return {
            'bytes': self.bytes(),
            'requests': self.requests(),
            'views': self.views(),
            'bytes_ratio': self.bytes_ratio(),
            'requests_ratio': self.requests_ratio(),
        }


if __name__ == "__main__":
    file = json.load(open(sys.argv[1], 'r'))
    cf = CFProcess(file)
    print(json.dumps(cf.all()))
