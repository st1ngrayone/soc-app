import pika
from config import Config

class Consumer:

    def __init__(self) -> None:
#        url = 'amqps://khojuydk:Aum_rfrrjPMlV1ROfMc15Hkj2B3YBGIv@cow.rmq2.cloudamqp.com/khojuydk'
        url = Config.RMQ_URL
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='hello')  # Declare a queue

        channel.basic_consume('hello', self.callback, auto_ack=True)

        print(' [*] Waiting for messages:')
        channel.start_consuming()
        connection.close()

    @staticmethod
    def callback(ch, method, properties, body):
        print(" [x] Received " + str(body))


if __name__ == '__main__':
    consumer = Consumer()
