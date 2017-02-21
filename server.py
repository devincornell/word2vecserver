
# server.py
import gensim
from flask import Flask
import json



app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/getvec/<word>')
def getvec(word):
    resp = {'word':word}
    resp['vec'] = list(map(float,model[word]))
    resp['status'] = 'good'
    
    return json.dumps(resp)

@app.route('/mostsimilar', methods=['GET'])
def mostsimilar():
    try:
        pos = json.loads(request.args.get('positive'))
        neg = json.loads(request.args.get('negative'))
        topn = json.loads(request.args.get('topn'))
    except KeyError:
        return json.dumps({'status':'error'})
    
    resp['similar'] = model.most_similar(positive=pos,negative=pos,topn=topn)
    resp['status'] = 'good'
    
    return json.dumps(resp)

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id

if __name__ == "__main__":
    print('Loading corpus..')
    fname = "data/GoogleNews-vectors-negative300.bin"
    #model = gensim.models.Word2Vec.load_word2vec_format(fname, binary=True)
    with open('data.json', 'r') as f:
        model = json.load(f)
    #print('king', model['king'])
    #print('queen', model['queen'])
    #print('male', model['male'])
    #print('female', model['female'])


    print('Runnin server..')
    app.run()
