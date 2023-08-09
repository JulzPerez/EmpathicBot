import random
import sys
from flask import Flask, render_template, request, session, redirect, url_for,flash

import os
import pandas as pd
import numpy as np

from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelWithLMHead.from_pretrained("julietoperez/gpt2-ft-ael")


app = Flask(__name__)

app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23',
                  ENV='development')

if __name__=='__main__':
   
    app.run()


def getPromptCompletion(prompt):

    #prompt = "Im really struggling with this math concept. I just can't seem to understand it."
    fine_tuned_model = pipeline('text-generation', model=model, tokenizer=tokenizer, max_new_tokens=100)
    res = fine_tuned_model(prompt)
    #print(res[0]['generated_text'])


    res = res[0]['generated_text'].strip(prompt)
    print(res)
    
    return res


def chatbot_response(msg):
    res = getPromptCompletion(msg)
    return res

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/")
def index():
    
    if request.method == 'GET':
        return render_template("index.html")

@app.route("/getResponse")
def get_bot_response():
    userText = request.args.get('msg')        
    return chatbot_response(userText.lower())

@app.route("/setClient")
def set_client():
    if session.get('current_client'):
        if session['current_client']!="":
            return "already set"

    session['current_client'] = request.args.get('client')
    session['current_msg_level']='generic'
    
    return "ok"

@app.route("/clearSessions")
def clear_sessions():
    # session.pop('current_client', None)
    # session.pop('current_msg_level', None)
    session['current_client']=''
    session['current_msg_level'] = 'generic'
    return "ok"



