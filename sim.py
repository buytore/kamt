from gensim import corpora, models, similarities
from os import listdir
from os.path import isfile, join
from collections import defaultdict
from pprint import pprint

path = "KAMTData"
files = [f for f in listdir(path) if isfile(join(path, f))]

documents = []
for f in files:
    file = open(path+"/"+f, 'r')
    documents.append(file.read())
    file.close()

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]


frequency = defaultdict(int)
for text in texts:
     for token in text:
         frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
          for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('tmp/deerwester.dict') # store the dictionary, for future reference
#print(dictionary)

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('tmp/deerwester.mm', corpus) # store to disk, for later use

dictionary = corpora.Dictionary.load('tmp/deerwester.dict')
corpus = corpora.MmCorpus('tmp/deerwester.mm')
#print(corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=34)


from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def initial():
    return '<form action="/ask" method="POST"><input name="text" size = "200"><input type="submit" value="Go"></form>'

@app.route("/ask", methods=['POST'])
def ask():
    directResponse = ''
    askText = request.form['text']
    if askText != '':
        doc = askText
        vec_bow = dictionary.doc2bow(doc.lower().split())
        vec_lsi = lsi[vec_bow]  # convert the query to LSI space
        print(vec_lsi)

        index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
        index.save('tmp/deerwester.index')
        index = similarities.MatrixSimilarity.load('tmp/deerwester.index')

        sims = index[vec_lsi]  # perform a similarity query against the corpus
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        print(sims)
        if sims[0][1]==0: response = 'I could not find a good answer for you, please explain more about what you are doing.'
        else:
            response = "You may find the tool that your are looking for \n" \
                       "in one or few of the following deliverables (please note the deliverable column)." \
                       "If the results did not help you please" \
                       " navigate manually."
            for i in range(10):
                response += " " + str(i + 1) + " " + (documents[sims[i][0]].split(":")[0])
                directResponse += (documents[sims[i][0]].split(":")[0]) + ';'
    else:
        response = "You did not enter anything!"
    response += '<form action="/"><input type="submit" value="Let me try again"></form>'
    return response




if __name__ == "__main__":
    app.run(host='0.0.0.0')#

'''
doc = askText
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
index.save('tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('tmp/deerwester.index')

sims = index[vec_lsi] # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims)

response = documents[sims[0][0]].split(":")[0]

print response
'''
'''




        response = "You may find the tool that your are looking for \n" \
               "in the following section."
    response += "... '" + (documents[sims[0][0]].split(":")[0]) + "'"
    response += "... if the result does not satisfy your needs please navigate manually. "
    return response
'''
