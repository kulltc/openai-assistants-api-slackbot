import configparser
import os
from pathlib import Path

# get the absolute path of the current script
script_location = Path(os.path.abspath(__file__))

# get the directory containing the script
script_dir = script_location.parent

# construct the full path to the config file
config_file = script_dir / 'config.ini'

# load the config parser
config = configparser.ConfigParser()
config.read(config_file)

os.environ["SLACK_APP_TOKEN"] = config.get('slack', 'app_token')
os.environ["SLACK_BOT_TOKEN"] = config.get('slack', 'bot_token')
os.environ["SLACK_CHANNELS"] = config.get('slack', 'allowed_channels')
os.environ["RABBITMQ_HOST"] = config.get('rabbitmq', 'host')
os.environ["RABBITMQ_QUEUE"] = config.get('rabbitmq', 'queue')
os.environ["RABBITMQ_USER"] = config.get('rabbitmq', 'user')
os.environ["RABBITMQ_PASSWORD"] = config.get('rabbitmq', 'password')
os.environ["OPENAI_API_KEY"] = config.get('openai', 'api_key')
os.environ["OPENAI_ASSISTANT_ID"] = config.get('openai', 'assistant_id')
os.environ['ASSISTANT_ID_STORAGE_CLASS'] = config.get('openai', 'assistant_storage')
os.environ["SQL_ROOT_DIR"] = config.get('file_locs', 'sql_root')
os.environ["TABULAR_FILE_LOCATION"] = config.get('file_locs', 'tabular_file_loc')