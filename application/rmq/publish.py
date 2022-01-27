import pika
from config import Config

class Producer(object):
    def __init__(self):
        url = Config.RMQ_URL
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()  # start a channel
        self.channel.queue_declare(queue='hello')  # Declare a queue

#        connection.close()

    def send(self, data):
        self.channel.basic_publish(exchange='', routing_key='hello', body=data)


if __name__ == '__main__':
    producer = Producer()
    producer.send('Hello CloudAMQP111!')
    print(" [x] Sent 'Hello CloudAMQP!'")
