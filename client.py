
import http.client
import json
import numpy as np

class WTVClient():
    def __init__(self, domain='localhost', port=5000, timeout=2):
        self.conn = http.client.HTTPConnection(domain,port)

    def getvector(self, word):

        self.conn.request('GET', '/getvec/' + str(word))

        r = self.conn.getresponse()
        if r.status == 200:
            d = json.loads(r.read().decode('utf-8'))
            vec = np.array(d['vec'])
        else:
            vec = None
        return vec


if __name__ == '__main__':
    wtv = WTVClient()

    kv = wtv.getvector('king')
    qv = wtv.getvector('queen')

    print('king norm:', np.linalg.norm(kv))
    print('queen norm:', np.linalg.norm(qv))
    print('cosine similarity:', np.dot(kv,qv)/(np.linalg.norm(kv)*np.linalg.norm(qv)))