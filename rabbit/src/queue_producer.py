import time
import pika

# Rabbit MQ queue test
def main():
    # Create a RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="messaging"))
    channel = connection.channel()

    # Get the RabbitMQ "hello" queue
    channel.queue_declare(queue="hello")

    print('Starting to send messages to the "hello" queue')

    count = 0

    # Send a message to the RabbitMQ "hello" queue each second
    while True:
        print(f"Sending message {count}.")
        channel.basic_publish(
            exchange="",
            routing_key="hello",
            body=f"Sending message {count}.",
        )

        time.sleep(1)
        count += 1


if __name__ == "__main__":
    main()
