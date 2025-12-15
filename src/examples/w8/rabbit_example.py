import pika

def callback(ch, method, properties, body):
    print(f" - Received: {body}")

credentials = pika.PlainCredentials("user", "password")

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost",
                              port=5672,
                              connection_attempts=3,
                              retry_delay=5,
                              credentials=credentials
    )
)
channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange="", routing_key="hello", body="Hello world!"
)

channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=callback)

print("waiting ...")

channel.start_consuming()