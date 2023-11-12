from .slackbot.slack_app import SlackBot

def main():
    slackbot = SlackBot()
    slackbot.start()

if __name__ == "__main__":
    main()
