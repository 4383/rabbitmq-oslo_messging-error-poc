import sys
from kombu import Connection, Exchange, Consumer, Queue
from process_message import process_message

def consumer():
    rabbit_host = "amqp://{host}:5672/".format(host=sys.argv[1])
    print("Connection to {host}".format(host=rabbit_host))
    
    # Create the connection
    conn = Connection(rabbit_host)
    
    # Create the exchange
    test_exchange = Exchange("test_exchange", type="direct")
    
    # Create the queue
    queue = Queue(name="queue", exchange=test_exchange, routing_key="test")
    
    # Create the consumer
    with Consumer(conn, queues=queue, callbacks=[process_message], accept=["text/plain"]):
        conn.drain_events()


if __name__ == "__main__":
    consumer()
