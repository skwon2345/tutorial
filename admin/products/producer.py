import json
import pika  # package to send events to RabbitMQ

params = pika.URLParameters(
    "amqps://uvznzatz:0hrHHWQvv-jfx31b-VHKsz8ie7GfGqjM@dingo.rmq.cloudamqp.com/uvznzatz"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange="", routing_key="main", body=json.dumps(body), properties=properties)
