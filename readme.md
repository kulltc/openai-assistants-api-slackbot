# Tabular and SQL GPT Assistant
## Overview
The Tabular and SQL GPT Assistant is an AI-powered tool designed to assist developers in troubleshooting and understanding (Tabular Model) data warehouse projects. It focuses on two critical layers: the SQL Data Warehouse and the Tabular Model (SSAS), which sits atop the SQL Server.

## Key Features:
- Code Insight Functions: Offers functions to access and analyze source code of both SQL and Tabular layers.
- Knowledge Database: The AI builds out a knowledge base as it goes, making it more efficient and knowledgeable the more you use it.  

## Usage
- Go to api.slack.com and create a slack app. Create application and Bot tokens.
- Install bot to the Slack workspace (you may want to use a personal testing workspace first, which are free to create).
- Create a channel in your Slack workspace, add the bot and copy the channel ID.
- Copy config.ini.default to config.ini and complete configs, add the channel ID to allowed_channels.
- Test functionality by navigating to the root folder of the app and run `python -m app.test`
- Open two CLI windows, and start both `python -m app.slack_listener` and `python -m app.rabbit_msq_consumer`.
- Send a message from the slack channel, make sure to @ mention the bot.

## License
This project is licensed under the MIT License

## Support
For support, please open an issue in the repository, or contact the maintainers directly.
