import pika

# Rabbit MQ queue test
def main():
    # Create a RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="messaging"))
    channel = connection.channel()

    # Create a RabbitMQ queue
    channel.queue_declare(queue="hello")

    # Create a RabbitMQ callback
    def callback(ch, method, properties, body):
        print(
            f"[x] Received {body.decode('utf-8')}",
        )

    # Consume the RabbitMQ queue
    channel.basic_consume(
        queue="hello",
        on_message_callback=callback,
        auto_ack=True,
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
