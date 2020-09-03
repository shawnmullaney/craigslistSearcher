#!/usr/bin/python3
import requests
import os
from craigslist import CraigslistEvents
from craigslist import CraigslistForSale
import json
import smtplib
from CREDS import gmail_user, gmail_password

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

for result in cl_s.get_results(sort_by='newest'):
    formatted = result["datetime"] + " " + result["name"] + " " + result["price"]
    print(formatted)
    mail_body.append(formatted)

for result2 in cl_free.get_results(sort_by='newest'):
    formatted2 = result2["datetime"] + " " + result2["name"] + " " + result2["price"]
    print(formatted2)
    mail_body.append(formatted2)


send_email('\n'.join(map(str, mail_body)))
