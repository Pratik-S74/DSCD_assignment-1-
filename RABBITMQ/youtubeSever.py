#!/usr/bin/env python
# coding: utf-8

import pika
import sys
import os
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='users', durable=True)
channel.queue_declare(queue='youtubers', durable=True)

users_subscriptions={}
youtubers_video={}

def consumer_user_request():
    def callback(ch, method, props, body):
        data=json.loads(body)
        #Handling login request
        if data['request'] == 'login':
            if data['user'] not in users_subscriptions:
                users_subscriptions[data['user']]=[]
                print("User data is uploaded")
            print(f"{data['user']} logged in")
        #Handling subscription/unsubscription request
        elif data['request'] == 'status':
            if data['subscribe'] == 'True':
                if data['youtuber'] in youtubers_video:
                    users_subscriptions[data['user']].append(data['youtuber'])
                    print(f"{data['user']} subscribed to {data['youtuber']}")
                else:
                    print("Youtuber does not exists..")
                #print(users_subscriptions[data['user']])
            else:
                if users_subscriptions[data['user']].count(data['youtuber'])!=0:
                    users_subscriptions[data['user']].remove(data['youtuber'])
                    print(f"{data['user']} unsubscribed to {data['youtuber']}")
                else:
                    print("Kindly subscribe the youtuber first")
    try:
        channel.basic_consume(queue='users', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    except KeyboardInterrupt:
        print("Terminated.")
    finally:
        pass


def consume_youtuber_requests():
    def callback(ch, method, props,body):
        data=json.loads(body)
        if data['youtuber'] not in youtubers_video:
            youtubers_video[data['youtuber']]=[]
        youtubers_video[data['youtuber']].append(data['video'])
        print(f"{data['youtuber']} uploaded {data['video']}")
        #calling notify_users
        notify_users(data['youtuber'],data['video'])
    try:
        channel.basic_consume(queue='youtubers', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    
    except KeyboardInterrupt:
        print("Terminated.")
    finally:
        pass
    


def notify_users(youtuber,videoname):
    usersNotificaitionSentTo=[]
    #fetching the subscribed youtubers
    for user in users_subscriptions:
        Data=users_subscriptions.get(user)
        if Data.count(youtuber)!=0:
            usersNotificaitionSentTo.append(user)
    print(usersNotificaitionSentTo)
    for user in usersNotificaitionSentTo:
        notificationMessage = f"New Notification: {youtuber} uploaded {videoname}"
        #Making separate queue for each user
        channel.queue_declare(queue=user, durable=True)
        channel.basic_publish(exchange='', routing_key=user, body=notificationMessage, properties=pika.BasicProperties(
                         delivery_mode = pika.DeliveryMode.Persistent
                      ))


def main():
    #calling user_request
    consumer_user_request()
    #calling youtuber_request
    consume_youtuber_requests()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)






