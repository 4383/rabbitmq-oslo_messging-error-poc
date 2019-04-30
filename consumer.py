from kombu import Connection, Exchange, Consumer, Queue
from process_message import process_message

# Create the connection
conn = Connection("amqp://10.88.0.20:5672/")

# Create the exchange
test_exchange = Exchange("test_exchange", type="direct")

# Create the queue
queue = Queue(name="queue", exchange=test_exchange, routing_key="test")

# Create the consumer
with Consumer(conn, queues=queue, callbacks=[process_message], accept=["text/plain"]):
    conn.drain_events()
