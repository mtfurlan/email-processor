import email
from abc import ABC, abstractmethod


class PluginABC(ABC):
    # list of senders to handle
    senders: list[str]


    def canHandle(self, msg: email.message.EmailMessage) -> bool:
        return msg.senderRaw in self.senders

    # function to handle stuff
    @abstractmethod
    def handle(self, msg: email.message.EmailMessage) -> bool:
        raise NotImplementedError
