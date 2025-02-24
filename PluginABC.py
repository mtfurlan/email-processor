import email.message
from abc import ABC, abstractmethod
import os
import toml


class PluginABC(ABC):
    # list of senders to handle
    senders: list[str]
    config: any = None # TODO ???

    def __str__(self):
        return type(self).__name__
    def __format__(self, format_spec: str) -> str:
        return str(self).__format__(format_spec)

    def __init__(self):
        # TODO: check senders list exists

        # janky bullshit to get filename from plugin
        name = type(self).__module__.replace("plugins.", "")
        confFile = f"config/{name}.toml"
        if os.path.isfile(confFile):
            self.config = toml.load(confFile)



    def canHandle(self, uid: int, msg: email.message.EmailMessage) -> bool:
        return msg.senderRaw in self.senders

    # function to handle stuff
    @abstractmethod
    def handle(self, uid: int, msg: email.message.EmailMessage) -> bool:
        raise NotImplementedError
