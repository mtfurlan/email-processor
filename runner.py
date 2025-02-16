#!/usr/bin/env python3

import os
import sys
import email
import email.policy
from dotenv import load_dotenv
from imapclient import IMAPClient
import importlib.util

load_dotenv()

#def import_from_path(module_name, file_path):
#    spec = importlib.util.spec_from_file_location(module_name, file_path)
#    module = importlib.util.module_from_spec(spec)
#    sys.modules[module_name] = module
#    spec.loader.exec_module(module)
#    return module
#
#
#dir_list = os.listdir(path)


server = IMAPClient("imap.gmail.com", use_uid=True)

server.login(os.getenv('USERNAME'), os.getenv('PASSWORD'))
select_info = server.select_folder('INBOX')
print('%d messages in INBOX' % select_info[b'EXISTS'])

messages = server.search()
for uid in messages:
    msg_data = server.fetch([uid], "RFC822")[uid][b'RFC822']
    msg = email.message_from_bytes(msg_data, policy=email.policy.default)
    import ipdb; ipdb.set_trace()
    simplest = msg.get_body(preferencelist=('plain', 'html'))
    content = simplest.get_content()
    print(uid, msg.get("From"), msg.get("Subject"))

    #archive
    #server.delete_messages([uid])

    import ipdb; ipdb.set_trace()
server.logout()
