#!/usr/bin/env python3

"""
author: Viktor Trokhymenko
e-mail: trokhymenkoviktor@gmail.com
project: bot
program: bot2.py
version: 2.0
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
flag = 0
buf = {}
qua_en = ['How many insights you want to get (maximum 3)?', 'How many messages send in one pool (maximum 5)?']
qua_ru = ['Сколько раз Вы хотите получать инсайты  (максимум 3)?', 'Сколько сообщений отправлять в одном пуле (максимум 5)?']
insite = [
    'Last 4 days your click-through rate (ctr) was higher than average by 1895.22% for all ads in adset ретаргетинг — Copy optimized for Landing Page Views', \
    'Last 3 days your cost per click (cpc) was higher than average by 56.84% in all ads optimized for Daily Unique Reach', \
    'Last 5 days your cost per action (cpa) was higher than average by 59.98% in all ads shown at 10 PM - 11 PM', \
    'Yesterday your click-through rate (ctr) was lower than average by 100.00% for all ads in adset E-comm Int — Copy optimized for Daily Unique Reach', \
    'Your pixel is getting data from several websites. Is it ok?', \
    'Last 7 days your conversion rate was higher than average by 33.11% in all ads shown at 01 PM - 02 PM', \
    'Last 2 days your click-through rate (ctr) was lower than average by 100.00% for male users for all ads in adset 6096146277001', \
    'Last 2 days your cost per click (cpc) was higher than average by 175.08% in ad 1_1 optimized for Daily Unique Reach', \
    'Last 2 days your click-through rate (ctr) was lower than average by 100.00% for all ads in adset 6096146276001', \
    'None of your adsets use delivery scheduling. You might be spending your budget not optimally.', \
    'Last 2 days your click-through rate (ctr) was lower than average by 100.00% in ad 6096146567401', \
    'Yesterday your click-through rate (ctr) was lower than average by 100.00% for all ads in adset 6096146276001 optimized for Daily Unique Reach', \
    'Last 1 days your click-through rate (ctr) was lower than average by 100.00% for all ads in adset 6096146276001 placed in Facebook and optimized for Daily Unique Reach', \
    'Last 2 days your click-through rate (ctr) was lower than average by 100.00% in ad 6096146566201', \
    'Yesterday your click-through rate (ctr) was lower than average by 100.00% for all ads in adset 6096146276001 placed in Facebook Right hand column and optimized for Daily Unique Reach']


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
                        #message = get_message()

                        #bot.send_text_message(recipient_id,message)

                        if flag == 0:

                            info_user = graph.get_object(id=recipient_id)
                            name = info_user['first_name']
                            locale = info_user['locale']
                            print(name,locale)

                            if locale == 'ru_RU':
                                message = 'Привет, {}'.format(name)
                                bot.send_text_message(recipient_id, message)

                                bot.send_action(recipient_id, action='typing_on')

                                bot.send_text_message(recipient_id, qua_ru[0])
                            else:
                                message = 'Hi, {}'.format(name)
                                bot.send_text_message(recipient_id, message)

                                bot.send_action(recipient_id, action='typing_on')

                                bot.send_text_message(recipient_id, qua_en[0])
                            flag = 1
                        elif flag == 1:
                            bot.send_text_message(recipient_id, '1')
                            flag = 2
                        elif flag == 2:
                            bot.send_text_message(recipient_id, '2')
                            flag = 3
                        elif flag == 3:

                            buf['q1'] = message
                            print('buf[q1]', buf['q1'])

                            bot.send_action(recipient_id, action='typing_on')

                            if ( (int(buf['q1']) >= 1) & (int(buf['q1']) <= 3)):

                                info_user = graph.get_object(id=recipient_id)
                                locale = info_user['locale']
                                if locale == 'ru_RU':
                                    bot.send_text_message(recipient_id, qua_ru[1])
                                else:
                                    bot.send_text_message(recipient_id, qua_en[1])

                                flag = 4
                            else:
                                bot.send_text_message(recipient_id, qua_en[0])
                                flag=2

                        elif flag == 4:
                            bot.send_text_message(recipient_id, '4')
                            flag = 5
                        elif flag == 5:

                            buf['q2'] = message
                            print('buf[q2]', buf['q2'])

                            bot.send_action(recipient_id, action='typing_on')

                            if ( (int(buf['q2']) >= 1) & (int(buf['q2']) <= 5)):

                                print('type',type(buf['q1']),type(buf['q2']))

                                #bot.send_text_message(recipient_id, buf['q2'])

                                st = 0
                                ed = int(buf['q2'])

                                #print('type', type(ed), type(int(buf['q2'])))

                                if int(buf['q1']) == 1:
                                    print('enter_1')
                                    bot.send_text_message(recipient_id, '. '.join(insite[:int(buf['q2'])]))
                                else:
                                    for i in range(1, int(buf['q1']) + 1):
                                        # for j in range(2,q_2+1):
                                        print('enter_',i)
                                        #print(insite[st:ed])

                                        bot.send_action(recipient_id, action='typing_on')

                                        bot.send_text_message(recipient_id, '. '.join(insite[st:ed]))

                                        st = ed
                                        ed = st + int(buf['q2'])

                                        if i==(int(buf['q1']) + 1):
                                            print('sleep_1')
                                            time.sleep(1)
                                        else:
                                            print('sleep_60')
                                            time.sleep(2)

                                flag = 6
                            else:
                                bot.send_text_message(recipient_id, qua_en[1])
                                flag=4
                        elif flag == 6:
                            print('flag0-6')
                            if int(buf['q1']) == 1:
                                flag=0
                            else:
                                flag = 7
                        elif flag == 7:
                            print('flag0-7')

                            if int(buf['q1']) == 2:
                                flag=0
                            else:
                                flag = 8
                        elif flag == 8:
                            print('flag0-8')

                            if int(buf['q1']) == 3:
                                flag=0
                            else:
                                flag = 9
                        elif flag == 9:
                            print('flag0-9')

                            flag = 10
                        print('flag->',flag)
                else:
                    pass

        return "Success"



def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!","We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
