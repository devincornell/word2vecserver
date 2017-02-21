
import http.client

class WTVClient():
    def __init__(self, domain='localhost', port=5000):
        self.conn = http.client.HTTPConnection(domain,port)

    def getvector(self, word):

        self.conn.request('GET', '//getword/' + str(word))

        r = self.conn.getresponse()

        print(r.status)

        return []


if __name__ == '__main__':
    wtv = WTVClient()

    print(wtv.getvector('china'))
