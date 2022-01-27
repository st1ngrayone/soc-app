import pika
from application.extensions import mysql
from config import Config

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = Config.RMQ_URL
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
def callback(ch, method, properties, body):
  print(" [x] Received " + str(body))

  def add_new_post(post: Post):
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute(
          'INSERT INTO posts VALUES (NULL, %s, %s, %s, %s, NULL)',
          (
              post.user_id,
              post.title,
              post.body,
              post.created_at
          )
      )
      mysql.connection.commit()


channel.basic_consume('hello',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()