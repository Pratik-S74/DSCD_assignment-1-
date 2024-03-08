#!/usr/bin/env python
# coding: utf-8

import pika
import os
import json
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='users', durable=True)

user = sys.argv[1]

channel.queue_declare(queue=user, durable=True)


def receiveNotifications():
    def callback(ch, method, properties, body):
        decoded_message = body.decode('utf-8')
        print(decoded_message)
    try:
        channel.basic_consume(queue=user, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Terminated.")
    finally:
        pass


def updateSubscription(user_name, ytbr_name, s_status):
    if ytbr_name=="":
        data = {
            "request":"login",
            "user" : user_name
        }
    else:
        if s_status == 's':
            s_status='True'
        elif s_status == 'u':
            s_status = 'False'

        data = {
             "request":"status",
             "user" : user_name,
             "youtuber":ytbr_name,
             "subscribe":s_status
        }
        print(data)
    channel.basic_publish(exchange='', routing_key='users', body=json.dumps(data),
                         properties=pika.BasicProperties(
                         delivery_mode = pika.DeliveryMode.Persistent
                      ))
    print("SUCCESS")
    

if len(sys.argv) == 4:
    subscribed_s_status = sys.argv[2]
    youtuber = sys.argv[3]
    updateSubscription(user, youtuber, subscribed_s_status)
elif len(sys.argv) == 2:
    updateSubscription(user,"","")
    receiveNotifications()
else:
    print("Invalid number of arguments")
    sys.exit(1)





