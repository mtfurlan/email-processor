from abc import ABC
from typing import runtime_checkable, Protocol
import email

@runtime_checkable
class EmailProcessorProtocol(Protocol):
    def can_handle(self, msg: email.message.EmailMessage) -> bool:
        pass

    def handle(self, msg: email.message.EmailMessage) -> bool:
        pass
