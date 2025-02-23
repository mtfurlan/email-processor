import email.message
from abc import ABC, abstractmethod
import os
import toml


class PluginABC(ABC):
    # list of senders to handle
    senders: list[str]
    config: any = None # TODO ???

    def __init__(self):
        # janky bullshit to get filename from plugin
        name = type(self).__module__.replace("plugins.", "")
        confFile = f"config/{name}.toml"
        if os.path.isfile(confFile):
            self.config = toml.load(confFile)



    def canHandle(self, msg: email.message.EmailMessage) -> bool:
        return msg.senderRaw in self.senders

    # function to handle stuff
    @abstractmethod
    def handle(self, msg: email.message.EmailMessage) -> bool:
        raise NotImplementedError
