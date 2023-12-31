from .openai_assistant import ConversationsManager, SimpleStorage
from .openai_functions.sql_functions import search_sql_file, get_sql_file
from .openai_functions.tabular_functions import get_tabular_measure

# Usage example
print(search_sql_file("some_file.sql"))
print(get_tabular_measure("measurename"))


## Uncomment and update the section below for testing conversations.

# storage = SimpleStorage()
# conversation_manager = ConversationsManager(storage)
# print(f"A1: {response}")
# response = conversation_manager.continue_conversation(external_id="B", user_input="Hello, this is conversation 'B', please simply acknowledge you received this message with 'OK'.")
# print(f"B1: {response}")
# response = conversation_manager.continue_conversation(external_id="A", user_input="What conversation is this please?")
# print(f"A2: {response}")
# response = conversation_manager.continue_conversation(external_id="B", user_input="What conversation is this please?")
# print(f"B2: {response}")