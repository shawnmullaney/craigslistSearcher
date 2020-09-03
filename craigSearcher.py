#!/usr/bin/python3
import requests
import os
from craigslist import CraigslistEvents
from craigslist import CraigslistForSale
import json
import smtplib
from CREDS import gmail_user, gmail_password

def check(fname, txt):
    with open(fname) as dataf:
        return any(txt in line for line in dataf)

def send_email(posts):
    body = posts
    subject = 'Craigslist Alert'
    message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (gmail_user, gmail_user, subject, body)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_user, message)
        server.close()
        print("Email Sent!")
    except:
        print("Failed to send mail")


#CraigslistForSale.show_filters(category='sss')
#cl_e = CraigslistEvents(site='wenatchee', filters={'free': True, 'food': True})
cl_s = CraigslistForSale(site='wenatchee', category='sss', filters={'posted_today': False, 'search_titles': True, 'has_image': True, 'query': "fridge", 'max_price':100,})
cl_free = CraigslistForSale(site='wenatchee', category='zip', filters={'posted_today': False, 'query': "fridge", 'query': "air conditioner", 'query': "dishwasher", 'query': "hydroponic", 'query': "table", 'query': "desk"})

mail_body = []
sent_list = []

for result in cl_s.get_results(sort_by='newest'):
    if not check('sentlist.txt', result["id"]):
        #if result["id"] not in all_lines:
        formatted = result["id"] + " " + result["datetime"] + " " + result["name"] + " " + result["price"]
        print(formatted)
        mail_body.append(formatted)
        sent_list.append(result["id"] + "\n")
        with open("sentlist.txt",'a') as w:
            w.write(result["id"] + "\n")

for result2 in cl_free.get_results(sort_by='newest'):
    if not check('sentlist.txt', result2["id"]):
        #if result2["id"] not in all_lines:
        formatted2 = result2["id"] + " " + result2["datetime"] + " " + result2["name"] + " " + result2["price"]
        print(formatted2)
        mail_body.append(formatted2)
        #sent_list.append(result2["id"] + "\n")
        with open("sentlist.txt",'a') as w:
            w.write(result2["id"] + "\n")

if mail_body:
    send_email('\n'.join(map(str, mail_body)))
else:
    print("List empty. No mail for you.")
