from flask import Flask, request, jsonify, render_template
from nltk.corpus import wordnet
import pandas as pd
from nltk import word_tokenize
from nltk import WordNetLemmatizer,pos_tag
from nltk.corpus import stopwords
import string
import numpy as np
import pickle

app = Flask(__name__)
stop=stopwords.words("english")
punct=list(string.punctuation)
stop+=punct
def simpletag(tag):
    if tag.startswith("J") :
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN
aka=WordNetLemmatizer()
def cleanreview(words):
    output=[]
    for w in words :
        if not w.lower() in stop:
            tag=pos_tag([w])
            output.append(aka.lemmatize(w,pos=simpletag(tag[0][1])).lower())
    return output 
features=np.loadtxt("word.csv",delimiter=",",encoding="utf-8",dtype='str')
def get(x):
    output={}
    x=set(x)
    for words in features:
        output[words]=words in x
    return output    
def output_str(s):
    s=word_tokenize(s)
    s=cleanreview(s)
    s=get(s)
    loaded_model = pickle.load(open('finalized_model1.sav', 'rb'))
    result = loaded_model.classify(s)
    return result
    
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    data = request.form['comment']
    review = output_str(data)
    return render_template('answer.html',info=review)

if __name__ == '__main__':
    app.run()