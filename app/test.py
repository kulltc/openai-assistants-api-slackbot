from .openai_assistant import ConversationsManager, SimpleStorage
from .openai_functions.sql_functions import search_sql_file, get_sql_file
# Usage example
storage = SimpleStorage()
conversation_manager = ConversationsManager(storage)
response = conversation_manager.continue_conversation(external_id="A", user_input="Hello, this is conversation 'A', please simply acknowledge you received this message with 'OK'.")
print(f"A1: {response}")
response = conversation_manager.continue_conversation(external_id="B", user_input="Hello, this is conversation 'B', please simply acknowledge you received this message with 'OK'.")
print(f"B1: {response}")
response = conversation_manager.continue_conversation(external_id="A", user_input="What conversation is this please?")
print(f"A2: {response}")
response = conversation_manager.continue_conversation(external_id="B", user_input="What conversation is this please?")
print(f"B2: {response}")


