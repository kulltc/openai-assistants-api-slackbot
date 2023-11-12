# slack_app.py
import os
import json
import pika
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

class SlackBot:
    def __init__(self):
        self.app = App()
        self.allowed_channels = os.environ["SLACK_CHANNELS"].split(',')

        @self.app.event({"type": "app_mention", "subtype": None})
        def handle_messages_event(body, say, logger):
            self.handle_app_mention(body, say, logger)

    def handle_app_mention(self, body, say, logger):
        event = body["event"]

        # Check if the message is from a bot or already in a thread
        if event.get("subtype") == "bot_message":
            return
        print(event["text"])
        # Check for direct mention of the bot
        if event["channel"] in self.allowed_channels:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=os.environ["RABBITMQ_HOST"],
                credentials=pika.PlainCredentials(os.environ["RABBITMQ_USER"], os.environ["RABBITMQ_PASSWORD"])
            ))
            channel = connection.channel()
            channel.queue_declare(queue=os.environ["RABBITMQ_QUEUE"])

            # Include thread_ts if available, or use ts as the thread identifier
            event["thread_id"] = event.get("thread_ts", event["ts"])

            channel.basic_publish(exchange='', routing_key=os.environ["RABBITMQ_QUEUE"], body=json.dumps(event))
            connection.close()

    def start(self):
        handler = SocketModeHandler(self.app, os.environ["SLACK_APP_TOKEN"])
        handler.start()
