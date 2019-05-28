import sys
import time
from kombu import Connection, Exchange, Consumer, Queue
from process_message import process_message

def heartbeat_check():
    print("Heartbeat check")
    rabbit_host = "amqp://{host}:5672/".format(host=sys.argv[1])
    print("Connection to {host}".format(host=rabbit_host))
    
    # Create the connection
    conn = Connection(rabbit_host)
    
    # Create the exchange
    test_exchange = Exchange("test_exchange", type="direct")
    
    # Create the queue
    queue = Queue(name="queue", exchange=test_exchange, routing_key="test")
    
    while True:
        print("hb ping")
        conn.heartbeat_check(rate=5)
        conn.drain_events(timeout=0.01)
        print("hb pong")
        time.sleep(10)


if __name__ == "__main__":
    heartbeat_check()
