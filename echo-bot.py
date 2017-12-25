#!/usr/bin/env python3

"""
author: Viktor Trokhymenko
e-mail: trokhymenkoviktor@gmail.com
project: bot
program: echo-bot.py
version: 0.0
data: 12/2017
"""

import os, sys,json
import time
import random
from flask import Flask, request
from pymessenger import Bot, Button
from fbmq import Page,Template
import requests
import facebook
from collections import defaultdict

app = Flask(__name__)
PAGE_ACCES_TOKEN = 'your_token'
VERIFY_TOKEN = 'hello'

bot = Bot(PAGE_ACCES_TOKEN)
graph = facebook.GraphAPI(PAGE_ACCES_TOKEN)

a = defaultdict(list)
@app.route("/", methods=['GET', 'POST'])
def hello():
    global flag
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':


        data = request.get_json()
        print(data)

        for event in data['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']

                        bot.send_action(recipient_id, action='typing_on')

                        bot.send_text_message(recipient_id,message)

        return "Success"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
