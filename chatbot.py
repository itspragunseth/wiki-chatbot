
#Meet Robo: your friend

#import necessary libraries
import io
import time
import random
import string # to process standard python strings
import warnings
import numpy as np
import bs4
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
warnings.filterwarnings('ignore')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
s = ''
class ClearApp(App):

    def build(self):
        self.box = BoxLayout(orientation='horizontal', spacing=20)
        self.txt = TextInput(hint_text='Write here', size_hint=(.5,.1))
        print(self.txt)
        self.btn = Button(text='Send', on_press=self.clearText, size_hint=(.1,.1))
        self.box.add_widget(self.txt)
        self.box.add_widget(self.btn)

        return self.box

    def clearText(self, instance):
        global s
        print(self.txt.text) 
        s = self.txt.text
        self.txt.text = ''
        App.get_running_app().stop()

ClearApp().run()
time.sleep(3)
#Reading in the corpus
#s = input("Give me a keyword \n")
print(s)
wiki = "https://en.wikipedia.org/wiki/" + s
response = requests.get(wiki)

if response is not None:
    html = bs4.BeautifulSoup(response.text, 'html.parser')

    title = html.select("#firstHeading")[0].text
    paragraphs = html.select("p")
    #for para in paragraphs:
     #   print (para.text)

    # just grab the text up to contents as stated in question
    intro = '\n'.join([ para.text for para in paragraphs[0:5]])
    # print (intro)
    with io.open(s+ ".txt", "a", encoding="utf-8") as file23:
        file23.write(intro)
        file23.close()

z = s + ".txt"
with open(z,'r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("ROBO: I will answer your queries about "+s+". If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("ROBO: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("ROBO: "+greeting(user_response))
            else:
                print("ROBO: ",end="")
                print(response(user_response))
                out = response(user_response)
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("ROBO: Bye! take care..")