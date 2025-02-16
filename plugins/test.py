import email

class Plugin():
    def can_handle(self, msg: email.message.EmailMessage) -> bool:
        return False

    def handle(self, msg: email.message.EmailMessage) -> bool:
        return False
