import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import wikipedia

class Retrieval():
    def __init__(self):
        topics = ['stemming', 'Inverted index', 'Lemmatisation', 'Precision and recall', 'Lexical analysis', 'Text normalization','n-gram', 'Wildcard character', 'Edit distance', 'Levenshtein distance','Zipfs law', 'tf–idf','Vector space model','Stop words', 'PageRank' ]
        text =""
        for topic in topics:
            text += wikipedia.page(topic).content
        text = text.lower()
        self.sent_tokens = nltk.sent_tokenize(text)# converts to list of sentences
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemTokens(self,tokens):
        lemmer = nltk.stem.WordNetLemmatizer()
        return [lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self,text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def response(self, user_response):
        user_response = user_response.lower()
        robo_response=''
        temp_tokens = self.sent_tokens
        temp_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(temp_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0):
            robo_response=robo_response+"I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response+self.sent_tokens[idx]
            return robo_response
