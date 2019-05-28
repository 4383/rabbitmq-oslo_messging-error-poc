import sys
from kombu import Connection, Exchange, Producer

def producer():
    rabbit_host = "amqp://{host}:5672/".format(host=sys.argv[1])
    print("Connection to {host}".format(host=rabbit_host))
    
    # Create the connection
    conn = Connection(rabbit_host)
    
    # Create a new channel
    channel = conn.channel()
    
    # Create the exchange
    test_exchange = Exchange("test_exchange", type="direct")
    
    # Create the producer
    producer = Producer(exchange=test_exchange, channel=channel,
                        routing_key="test")
    
    # Publish a message
    producer.publish("Hello World!")


if __name__ == "__main__":
    producer()
