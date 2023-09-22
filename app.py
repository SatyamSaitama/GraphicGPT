import os

import openai
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

openai.api_key = "Your API Key"

app = Flask(__name__)
bootstrap = Bootstrap(app)
openai.api_key = os.environ.get(
    "Your API Key")


def completion(msg):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=msg, temperature=0)
    return res.choices[0].message["content"]


@app.route('/')
def index():
    openai.api_key = "Your API Key"

    return render_template('chatbot.html')








system = """
You are an Ai assistant who gives response in html. Every response should always be inside html tags.
User Can ask you to draw chart . Use chart js or Other library to draw charts.
Example 
***
User : Hi , can you write code in python print name
You : <code>print(USER)</code>
User : Can you draw chart for linear equations
You : Using chartjs you write the entire html and draw chart . The canvas should not be too big . It should fit the chat window . Its same size of like how whatsapp is.
***
"""
messages = [
    {'role': 'system', 'content': f'{system}'},
]


@app.route('/', methods=['POST'])
def process_query():
    openai.api_key = "Your Api Key"

    prompt = request.json['query']
    messages.append({'role': 'user',
                     'content': f"{prompt}"})

    response_text = completion(messages)
    print(response_text)
    f = open("templates/data.html", 'w', encoding='utf-8')
    f.write(response_text)
    f.close()
    messages.append({'role': 'assistant',
                     'content': f" {response_text}"})
    return {"response": response_text}


@app.route('/main')
def response():
    return render_template('data.html')


if __name__ == '__main__':
    app.run(debug=True, port=2200)
