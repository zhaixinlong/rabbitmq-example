#!/usr/bin/env python
import pika
import sys

import cfg

parameters = pika.URLParameters(cfg.url)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
 
# durable=True 持久化
channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=True)

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print("emit [x] Sent %r" % message)
connection.close()