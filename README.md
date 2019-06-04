# oslo.messaging and rabbitmq POCs

Some pieces of code to test things between python/oslo.messaging/rabbitmq.

See the use cases below to use this project.

## [Fix] switch rabbit connections
Fix switch connection destination when a rabbitmq cluster node disappear 

In a clustered rabbitmq when a node disappears, we get a ConnectionRefusedError
because the socket get disconnected. The socket access yields a OSError because
the heartbeat tries to reach an unreachable host (No route to host).

Catch these exceptions to ensure that we call ensure_connection for switching
the connection destination.

### Run the POC
```shell
$ git clone git@github.com:4383/rabbitmq-oslo_messging-error-poc
$ cd rabbitmq-oslo_messging-error-poc
$ python -m virtualenv .
$ source bin/activate
$ pip install -r requirements.txt
$ sudo podman run -d --hostname my-rabbit --name rabbit rabbitmq:3
$ python poc.py $(sudo podman inspect rabbit | niet '.[0].NetworkSettings.IPAddress')
```

And in parallele in an another shell|tmux:
```shell
$ podman stop rabbit
$ # observe the output of the poc.py script we now call ensure_connection
```

Now you can observe some output relative to the connection who is modified and
not catched before these changes.

Related to:
- https://bugs.launchpad.net/oslo.messaging/+bug/1828841
- https://bugzilla.redhat.com/show_bug.cgi?id=1665399

## [Tests] rabbitmq producer/consumer
Test python/rabbitmq producer and consumer.

The producer publish data on the rabbitmq server and the consumer
consum these datas.

### Run the test

Setup your env:
```shell
$ git clone git@github.com:4383/rabbitmq-oslo_messging-error-poc
$ cd rabbitmq-oslo_messging-error-poc
$ python -m virtualenv .
$ source bin/activate
$ pip install -r requirements.txt
$ sudo podman run -d --hostname my-rabbit --name rabbit rabbitmq:3
```

Run your consumer:
```shell
$ python consumer.py $(sudo podman inspect rabbit | niet '.[0].NetworkSettings.IPAddress')
```

And in parallele in an another shell|tmux:
```shell
$ python producer.py $(sudo podman inspect rabbit | niet '.[0].NetworkSettings.IPAddress')
```

### Further reading

For more examples you can read [my blog post on how to play with rabbitmq and python](https://herve.beraud.io/rabbitmq/python/amqp/kombu/2019/05/28/play-with-rabbitmq-and-python.html)
