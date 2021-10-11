import pika  # package to send events to RabbitMQ

params = pika.URLParameters(
    "amqps://uvznzatz:0hrHHWQvv-jfx31b-VHKsz8ie7GfGqjM@dingo.rmq.cloudamqp.com/uvznzatz"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="main")


def callback(ch, method, properties, body):
    print("Received in main")
    print(body)


channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()

channel.close()
