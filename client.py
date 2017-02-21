
import http.client
import json
import numpy as np
from urllib.parse import quote_plus

class WTVClient():
    def __init__(self, domain='localhost', port=5000, timeout=2, verb=False):
        self.conn = http.client.HTTPConnection(domain,port)
        self.verb = verb

    def getvec(self, word):
        self.conn.request('GET', '/getvec?word=' + word)

        r = self.conn.getresponse()
        if r.status == 200:
            d = json.loads(r.read().decode('utf-8'))
            try:
                vec = d['vec']
            except KeyError:
                vec = None
            vec = np.array(vec)
        else:
            vec = None
        return vec


    def mostsimilar(self, pos=[], neg=[], topn=5):
        headers = {'positive':pos,'negative':neg, 'topn':topn}
        qdata = ''
        for k,v in headers.items():
            if str(type(v)) == "<class 'int'>":
                v = str(v)
            qdata += str(k) + '=' + quote_plus(json.dumps(v)) + '&'

        #qdata = list(map(str,map(quote_plus, qdata)))
        qstr = '/mostsimilar?' + qdata
        if self.verb: print('Sending:', qstr)
        self.conn.request('GET', qstr)
        r = self.conn.getresponse()
        if r.status == 200:
            d = json.loads(r.read().decode('utf-8'))
        else:
            d = None
        return d

if __name__ == '__main__':
    wtv = WTVClient(domain='salinas.cs.ucsb.edu', port=5000)

    print('Get vectors:')
    kv = wtv.getvec('king')
    qv = wtv.getvec('queen')

    print('Do some math:')
    print('king norm:', np.linalg.norm(kv))
    print('queen norm:', np.linalg.norm(qv))
    print('cosine similarity:', np.dot(kv,qv)/(np.linalg.norm(kv)*np.linalg.norm(qv)))

    print(wtv.mostsimilar(pos=['king','queen']))
