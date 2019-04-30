from kombu import Connection, Exchange, Producer

# Create the connection
conn = Connection("amqp://10.88.0.20:5672/")

# Create a new channel
channel = conn.channel()

# Create the exchange
test_exchange = Exchange("test_exchange", type="direct")

# Create the producer
producer = Producer(exchange=test_exchange, channel=channel,
                    routing_key="test")

# Publish a message
producer.publish("Hello World!")
