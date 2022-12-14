import time
import pika

# Rabbit MQ queue test
def main():
    # Create a RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="messaging"))
    channel = connection.channel()

    # Listen to the logs exchange
    channel.exchange_declare(exchange="logs", exchange_type="fanout")

    # Create a queue
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the logs exchange
    channel.queue_bind(exchange="logs", queue=queue_name)

    # Create a RabbitMQ callback
    def callback(ch, method, properties, body):
        print(
            f"[x] Received {body.decode('utf-8')}",
        )

    # Consume the RabbitMQ queue
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True,
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
