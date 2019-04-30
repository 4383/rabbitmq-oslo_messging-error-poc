def process_message(body, message):
    print("The following message has been received: %s" % body)

    # Acknowledge the message
    message.ack()
