import time
import pika

# Rabbit MQ queue test
def main():
    # Create a RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="messaging"))
    channel = connection.channel()

    # Declare exchange
    channel.exchange_declare(exchange="logs", exchange_type="fanout")

    print('Starting to send messages to the "logs" exchange')

    count = 0

    # Send a message to the RabbitMQ "logs" exchange each second
    while True:
        print(f"Sending message {count}.")
        channel.basic_publish(
            exchange="logs",
            routing_key="",
            body=f"Sending message {count}.",
        )

        time.sleep(1)
        count += 1


if __name__ == "__main__":
    main()
