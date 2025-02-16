from typing import runtime_checkable, Protocol
import email


@runtime_checkable
class EmailProcessorProtocol(Protocol):
    # list of senders to handle
    senders: list[str]

    # function to handle stuff
    def handle(self, msg: email.message.EmailMessage) -> bool:
        pass
