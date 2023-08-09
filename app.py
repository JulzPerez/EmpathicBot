import random
import sys
from flask import Flask, render_template, request, session, redirect, url_for,flash

'''
from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelWithLMHead.from_pretrained("julietoperez/gpt2-ft-ael")

'''
from huggingface_hub import InferenceClient
client = InferenceClient(model="jeppy20/gpt2-ft-ael", token="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")

app = Flask(__name__)

app.config.update(SECRET_KEY='osd(99092=36&462134kjKDhuIS_d23',
                  ENV='development')

if __name__=='__main__':
   
    app.run()


def getPromptCompletion(prompt):

    res_inf = client.text_generation(prompt, max_new_tokens=50)
    res_inf = res_inf.strip('"')
    
    result = ''
    res_inf = res_inf.split('.')

    for i in range(1,len(res_inf)):
        result += res_inf[i].strip('"') + ". "
   
   
    print(result)
    
    return result.strip("Teacher:")

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



