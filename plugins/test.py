import email.message

from PluginABC import PluginABC


class TestPluginThingy(PluginABC):
    senders = ["bingo@patreon.com"]

    def handle(self, uid, msg: email.message.EmailMessage) -> bool:
        print(f'processing msg[{uid}]: "{msg.get("From")}": "{msg.get("Subject")}"')
        return True
