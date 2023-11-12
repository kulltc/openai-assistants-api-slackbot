import openai
import time
import json
import os
import redis


# Import your existing modules
from .openai_functions.tabular_functions import get_tabular_measure, get_tabular_table, get_tabular_table_relationships
from .openai_functions.sql_functions import get_sql_file, search_sql_file
from .openai_functions.memory import store_memory, search_memory



# Define an interface for the storage class
class IStorage:
    def set_value(self, key, value):
        """ Set a value in storage with the given key. """
        raise NotImplementedError

    def get_value(self, key):
        """ Retrieve a value from storage using the given key. """
        raise NotImplementedError

# Redis implementation.
class RedisStorage(IStorage):
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set_value(self, key, value):
        self.client.set(key, value)

    def get_value(self, key):
        value = self.client.get(key)
        return value.decode('utf-8') if value else None
    
# A simple key-value pair storage class
class SimpleStorage(IStorage):
    def __init__(self):
        self.store = {}

    def set_value(self, key, value):
        """ Store a value with the given key. """
        self.store[key] = value

    def get_value(self, key):
        """ Return the value associated with the given key, or None if not found. """
        return self.store.get(key)

# Main ConversationsManager class
class ConversationsManager:
    def __init__(self, storage: IStorage):
        """ Initialize the manager with a storage instance. """
        self.storage = storage
        self.assistant_id = os.environ["OPENAI_ASSISTANT_ID"]

    def continue_conversation(self, external_id, user_input):
        """ Continue or start a new conversation based on an external ID. """
        thread_id = self.storage.get_value(external_id)

        if not thread_id:
            user_input = user_input + "\n\n ### END OF USER INPUT. FAQ info is listed below, you may use this to answer the question if relevant.\n " + search_memory(user_input)
            thread = openai.beta.threads.create(messages=[])
            self.storage.set_value(external_id, thread.id)
            thread_id = thread.id

        openai.beta.threads.messages.create(thread_id=thread_id, content=user_input, role='user')
        run = self._create_run(self.assistant_id, thread_id)

        while run.status not in ["completed", "failed"]:
            run = self._update_run_status(run, thread_id)

            if run.status == "requires_action":
                run = self._handle_required_action(run, thread_id)

        if run.status == "completed":
            messages = openai.beta.threads.messages.list(thread_id=thread_id)
            return messages.data[0].content[0].text.value
        else:
            return f"Error: {run.last_error}"

    def _create_run(self, assistant_id, thread_id):
        """ Create a run with the given assistant and thread ID. """
        return openai.beta.threads.runs.create(assistant_id=assistant_id, thread_id=thread_id)

    def _update_run_status(self, run, thread_id):
        """ Retrieve the current status of the run. """
        time.sleep(3)  # Adjust the sleep time as necessary
        return openai.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread_id)
        

    def _handle_required_action(self, run, thread_id):
        """ Process required actions for a run and submit tool outputs. """
        tool_outputs = self._process_tool_calls(run)
        print(tool_outputs)
        try:
            return openai.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs)
        except Exception as err:
            print('Error returning tool outputs:', err, run)
            raise err

    def _process_tool_calls(self, run):
        """ Process tool calls required by the run. """
        tool_outputs = []
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            try:
                output = globals()[function_name](**arguments)
            except Exception as err:
                output = {'error': str(err)}
            tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
        return tool_outputs

# Usage example
# storage = SimpleStorage()
# conversation_manager = ConversationsManager(storage)
# response = conversation_manager.continue_conversation(external_id="A", user_input="Hello, this is conversation 'A', please simply acknowledge you received this message with 'OK'.")
# print(f"A1: {response}")
# response = conversation_manager.continue_conversation(external_id="B", user_input="Hello, this is conversation 'B', please simply acknowledge you received this message with 'OK'.")
# print(f"B1: {response}")
# response = conversation_manager.continue_conversation(external_id="A", user_input="What conversation is this please?")
# print(f"A2: {response}")
# response = conversation_manager.continue_conversation(external_id="B", user_input="What conversation is this please?")
# print(f"B2: {response}")
