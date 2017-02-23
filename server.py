
# server.py
import gensim
from flask import Flask, request
import json
import urllib.parse



app = Flask(__name__)

@app.route("/")
def hello():
    with open('index.html') as f:
        resp = f.read()
    return resp

@app.route('/getvec', methods=['GET'])
def getvec():
    try:
        word = request.args.get('word')
    except KeyError:
        return {'status':'error','problem':'Must provide a word.'}
    
    try:
        vec = list(map(float,model[word]))
    except KeyError:
        return {'status':'error','problem':'Word not found.'}

    # build response
    resp = {'status':'good','word':word}
    resp['vec'] = vec
    
    return json.dumps(resp)

@app.route('/mostsimilar', methods=['GET'])
def mostsimilar():
    try:
        dat = {}
        headers = ['positive', 'negative', 'topn']
        for h in headers:
            dat[h] = urllib.parse.unquote(request.args.get(h))
            print(dat[h])
            dat[h] = json.loads(dat[h])
    except KeyError:
        return json.dumps({'status':'error'})
    
    print(dat)
    dat['topn'] = int(dat['topn'])
    resp = dict()
    resp['similar'] = model.most_similar(positive=dat['positive'],negative=dat['negative'],topn=dat['topn'])
    resp['status'] = 'good'
    
    return json.dumps(resp)

def runserver(domain='localhost', port=8080, fname='data/GoogleNews-vectors-negative300.bin'):
    realmodel = True
    #domain = '0.0.0.0'
    #port = 5000
    #fname = "data/GoogleNews-vectors-negative300.bin"
    
    global model
    if realmodel:
        print('Loading corpus..')
        model = gensim.models.Word2Vec.load_word2vec_format(fname, binary=True)

    else:
        with open('data.json', 'r') as f:
            model = json.load(f)

    print('Runnin server..')
    app.run(host=domain, port=port)

if __name__ == "__main__":
    fname = "data/GoogleNews-vectors-negative300.bin"
    runserver(domain='0.0.0.0', port=8080, filename=fname)
