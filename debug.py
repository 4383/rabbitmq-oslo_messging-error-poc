import argparse
import socket
import time
import threading

import kombu
import kombu.connection
import kombu.entity
import kombu.messaging

import pysnooper


class Connection(object):
    """Connection object."""

    pools = {}

    def __init__(self, ip):
        self.connection = kombu.connection.Connection(
            'amqp://{ip}:5672/'.format(ip=ip),
            heartbeat=2,
            transport_options={
                'confirm_publish': True,
                'client_properties': {
                    'capabilities': {
                        'authentication_failure_close': True,
                        'connection.blocked': True,
                        'consumer_cancel_notify': True
                    },
                },
            },
        )
        self._heartbeat_thread_job()

    def _heartbeat_check(self):
        self.connection.heartbeat_check()

    @pysnooper.snoop()
    def _heartbeat_thread_job(self):
        """Thread that maintains inactive connections
        """
        #while not self._heartbeat_exit_event.is_set():
        while True:

            try:
                try:
                    self._heartbeat_check()
                    try:
                        self.connection.drain_events(timeout=0.001)
                    except socket.timeout:
                        pass
                except (socket.timeout,
                        kombu.exceptions.OperationalError,
                        ConnectionRefusedError,
                        OSError) as exc:
                    print("fixed by calling ensure_connection")
            except Exception as exc:
                print("fired")
                print(type(exc))
                print(exc)
                print("end fired")

        time.sleep(30)
        print("sleeping now")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="rabbitmq server ip")

    args = parser.parse_args()
    ip = args.ip
    connection = Connection(ip)
