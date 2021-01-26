#!/usr/bin/env python
import pika

import cfg

parameters = pika.URLParameters(cfg.url)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# durable=True 持久化
channel.exchange_declare(exchange='logs', exchange_type='fanout', durable=True)

# exclusive=True 如果是excl，则设置durability没有意义，因为不管服务器挂了还是客户端主动/被动断开了，队列都会自动删除。
# auto-delete，其实可简单的认为是同理，即使非excl，则无论是服务器挂了还是全部消费者断开了，队列都会删除。
result = channel.queue_declare(queue='receive1', durable=True)
queue_name = result.method.queue
print("queue_name:" + queue_name)

channel.queue_bind(exchange='logs', queue=queue_name,routing_key=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print("receive1 [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()