#!/usr/bin/env python
# coding: utf-8

import pika
import os
import json
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='youtubers', durable=True)


def publish_video(youtuber,video):
    Data = {
         #"request": 'login',
         "youtuber": youtuber,
         "video": video
    }
    channel.basic_publish(exchange='', routing_key='youtubers', body=json.dumps(Data),
                         properties=pika.BasicProperties(
                         delivery_mode = pika.DeliveryMode.Persistent
                      ))
    print("SUCCESS: Video is uploaded.")

if len(sys.argv) != 3:
        print("Invalid number of arguments")
        sys.exit(1)
else:
    youtuber = sys.argv[1]
    video = sys.argv[2]


publish_video(youtuber,video)













