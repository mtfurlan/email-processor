import email


class Plugin:
    senders = ["bingo@patreon.com"]

    def handle(self, msg: email.message.EmailMessage) -> bool:
        return False
