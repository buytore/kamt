# all the imports
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json

###BIJAN's Core application and data imports and builds
from gensim import corpora, models, similarities
from os import listdir
from os.path import isfile, join
from collections import defaultdict
from pprint import pprint

# Chose data source
useExcel = True

if useExcel == True:
    from readExcel import busNeedToDeliverable, busNeedToSolution, deliverablesToBusNeed, \
        deliverablesToSolution, solutionToNeed, solutionToDel
    path = "KAMTData2"
else:
    from static.data.spData import dataRec, busNeedToDeliverable, busNeedToSolution, deliverablesToBusNeed, \
        deliverablesToSolution, solutionToNeed, solutionToDel
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

index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
index.save('tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('tmp/deerwester.index')

##MARK's build - the FLASK interface and required connectors to data
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

def getProjectData():
    from openpyxl import load_workbook
    # ------------Create the Dictionary for Solution to Deliverable, and solution to BusNeed-----------------
    wb = load_workbook(filename='static/data/ProjectTasks.xlsx', read_only=True)
    ws = wb['Tableau']
    rowsWB = []
    for row in ws.rows:
        r = []
        for cell in row:
            r.append(cell.value)
        rowsWB.append(r)
    rowsWB.pop()
    #rows = rows[1:]
    jsonProj = json.dumps(rowsWB, ensure_ascii=False)
    return jsonProj

def getAllData():
    json1 = json.dumps(busNeedToDeliverable, ensure_ascii=False)
    json2 = json.dumps(busNeedToSolution, ensure_ascii=False)
    json3 = json.dumps(deliverablesToBusNeed, ensure_ascii=False)
    json4 = json.dumps(deliverablesToSolution, ensure_ascii=False)
    json5 = json.dumps(solutionToNeed, ensure_ascii=False)
    json6 = json.dumps(solutionToDel, ensure_ascii=False)
    return json1, json2, json3, json4, json5, json6

def getWebListData():
    import urllib2
    response = urllib2.urlopen('https://share.ahsnet.ca/teams/kmqa/_vti_bin/owssvr.dll?Cmd=Display&XMLDATA=TRUE&List={9DC112D0-A174-4C6E-93A2-C46287E0530E}')
    html = response.read()
    print html

########### ROUTING OPTIONS ###############
@app.route("/wordtree")
def wordtree():
    json1, json2, json3, json4, json5, json6 = getAllData()
    return render_template('wordTree.html', **locals())

@app.route("/sankey")
def sankey():
    json1, json2, json3, json4, json5, json6 = getAllData()
    return render_template('sankey.html', **locals())

@app.route("/sankeyTest")
def sankeyTest():
    json1, json2, json3, json4, json5, json6 = getAllData()
    return render_template('sankeyAI.html', **locals())

@app.route("/hello")
def hello():
    return render_template('columnMap.html', **locals())

@app.route("/")
def home():
    return render_template('home.html', **locals())


@app.route("/sp")
def spRest():
    return render_template('index.html', **locals())

@app.route("/jf")
def jFiddle():
    return render_template('sankeyTest_JFiddle.html', **locals())

@app.route("/db")
def dashboard():
    jsonProj = getProjectData()
    return render_template('dashboard3.html', **locals())

@app.route("/tree")
def tree():
    return render_template('treeMapSTQ.html', **locals())

@app.route("/cmap")
def cmap():
    return render_template('cmap.html', **locals())

@app.route("/comapping")
def comapping():
    return render_template('comapping.html', **locals())

@app.route("/adobe-captivate")
def captivate():
    return render_template('adobe-captivate.html', **locals())

@app.route("/nvivo")
def nVivo():
    return render_template('nvivo.html', **locals())

@app.route("/lessonslearnedrepository")
def LessonsLearnedRespository():
    return render_template('LessonsLearnedRepository.html', **locals())

@app.route("/refworks")
def RefWorks():
    return render_template('refworks.html', **locals())

##THIS IS TEST STUFF FOR MULTIPLE ITEMS
@app.route("/iframeitem/<itemname>")
def iframeItems(itemname="joe"):
    #print "This is the iframeitem", itemname
    fileName = itemname + ".html"
    return render_template(fileName, **locals())

@app.route("/click")
def click():
    return render_template('getListData.html', **locals())

@app.route("/wordJS")
def wordJS():
    return render_template('wordTreeJS.html', **locals())


############################################################
# JS Capture and Test
############################################################
@app.route('/getmethod/<jsData>')
def get_javascript_data(jsData):
    print jsData
    directResponse = []
    askText = jsData
    if askText != '':
        doc = askText
        vec_bow = dictionary.doc2bow(doc.lower().split())
        vec_lsi = lsi[vec_bow]  # convert the query to LSI space
        # print(vec_lsi)

        sims = index[vec_lsi]  # perform a similarity query against the corpus
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # print(sims)
        if sims[0][1] == 0:
            response = 'I could not find a good answer for you, please explain more about what you are doing.'
        else:
            response = "You may find the tool that your are looking for \n" \
                       "in one or few of the following deliverables (please note the deliverable column)." \
                       "If the results did not help you please" \
                       " navigate manually."
            for i in range(10):
                response += " " + str(i + 1) + " " + (documents[sims[i][0]].split(":")[0])
                directResponse.append((documents[sims[i][0]].split(":")[0]))
    else:
        response = "You did not enter anything!"
    json1, json2, json3, json4, json5, json6 = getAllData()
    json7 = json.dumps(directResponse, ensure_ascii=False)
    # return render_template('sankeyAI.html', **locals())
    # response += '<form action="/"><input type="submit" value="Let me try again"></form>'
    # return response
    print "This is json7: ", json7
    print "This is json6: ", json6
    return jsData


## BIJAN's MAGIC
"""
@app.route("/int2")
def initial():
    return '<form action="/ask" method="POST"><input name="text" size = "200"><input type="submit" value="Go"></form>'
"""
@app.route("/ask", methods=['POST'])
def ask():
    directResponse = []
    askText = request.form['text']
    if askText != '':
        doc = askText
        vec_bow = dictionary.doc2bow(doc.lower().split())
        vec_lsi = lsi[vec_bow]  # convert the query to LSI space
        # print(vec_lsi)

        sims = index[vec_lsi]  # perform a similarity query against the corpus
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        # print(sims)
        if sims[0][1]==0: response = 'I could not find a good answer for you, please explain more about what you are doing.'
        else:
            response = "You may find the tool that your are looking for \n" \
                       "in one or few of the following deliverables (please note the deliverable column)." \
                       "If the results did not help you please" \
                       " navigate manually."
            for i in range(10):
                response += " " + str(i + 1) + " " + (documents[sims[i][0]].split(":")[0])
                directResponse.append((documents[sims[i][0]].split(":")[0]))
    else:
        response = "You did not enter anything!"
    json1, json2, json3, json4, json5, json6 = getAllData()
    json7 = json.dumps(directResponse, ensure_ascii=False)
    return render_template('sankeyAI.html', **locals())
    #response += '<form action="/"><input type="submit" value="Let me try again"></form>'
    #return response




if __name__ == "__main__":
    app.run(host='0.0.0.0')

