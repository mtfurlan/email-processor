import email.message

from PluginABC import PluginABC


class Plugin(PluginABC):
    senders = ["bingo@patreon.com"]

    def handle(self, msg: email.message.EmailMessage) -> bool:
        print("HI we process but fail")
        return False
