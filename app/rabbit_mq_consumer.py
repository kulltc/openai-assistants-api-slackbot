# rabbitmq_consumer.py
import os
import json
import pika

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .openai_assistant import ConversationsManager, SimpleStorage, RedisStorage

if (os.environ['ASSISTANT_ID_STORAGE_CLASS'] == 'RedisStorage'):
    storage = RedisStorage()
else:
    storage = SimpleStorage()

conversationsManager = ConversationsManager(storage)
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def handle_message(channel, method, properties, body):
    event = json.loads(body)

    userMessage = event["text"]
    threadId = event["thread_id"]  # Use thread_id from the event
    response = conversationsManager.continue_conversation(threadId, userMessage)
    
    try:
        # Ensure the response is posted in the same thread
        client.chat_postMessage(channel=event["channel"], thread_ts=threadId, text=response)
    except SlackApiError as e:
        print(f"Error sending message: {e}")

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.environ["RABBITMQ_HOST"],
        credentials=pika.PlainCredentials(os.environ["RABBITMQ_USER"], os.environ["RABBITMQ_PASSWORD"])
    ))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ["RABBITMQ_QUEUE"])

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=os.environ["RABBITMQ_QUEUE"], on_message_callback=handle_message)

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
