import json
import os

import django
import pika  # package to send events to RabbitMQ

# the below code should be added to solve the error --> queue_1    | django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
# this error occurs becuase this consumer.py is out of products folder so it cannot import Product from products.models
# So the below code should be located before from products.models import Product.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters(
    "amqps://uvznzatz:0hrHHWQvv-jfx31b-VHKsz8ie7GfGqjM@dingo.rmq.cloudamqp.com/uvznzatz"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="admin")


def callback(ch, method, properties, body):
    print("Received in admin")
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print("Product likes increased!")


channel.basic_consume(queue="admin", on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()

channel.close()
