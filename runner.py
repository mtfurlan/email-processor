#!/usr/bin/env python3

import os
import sys
import email
import email.policy
from dotenv import load_dotenv
from imapclient import IMAPClient
import importlib.util
from EmailProcessorProtocol import EmailProcessorProtocol
import glob
import re

load_dotenv()

pluginPath = "plugins"


def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


plugin_files = glob.glob(f"{pluginPath}/*.py")

plugins = []
for f in plugin_files:
    p = import_from_path(f, f).Plugin()
    if not isinstance(p, EmailProcessorProtocol):
        raise Exception(f"fuck your plugin {f}")
    plugins.append(p)


server = IMAPClient("imap.gmail.com", use_uid=True)

server.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
select_info = server.select_folder("INBOX")


print(f"processing {select_info[b'EXISTS']} messages from INBOX")

messages = server.search()
for uid in messages:
    msg_data = server.fetch([uid], "RFC822")[uid][b"RFC822"]
    msg = email.message_from_bytes(msg_data, policy=email.policy.default)
    simplest = msg.get_body(preferencelist=("plain", "html"))
    content = simplest.get_content()
    print(f'processing msg[{uid}]: "{msg.get("From")}": "{msg.get("Subject")}"')

    # sender might be something like '"Victoria Scott (via Patreon)" <bingo@patreon.com>'
    # we want to filter on the email portion
    msg.senderRaw = re.findall(r'^(?:".*" )?<?(.*?)>?$', (msg.get("X-Google-Original-From") or msg.get("From")))[0]
    #import ipdb; ipdb.set_trace()

    handled = False


    # TODO: move canHandle into plugin thingy and change it to ABC or whatever
    def canHandle(p, msg) -> bool:
        return msg.senderRaw in p.senders

    #results = plugins.filter(p => canHandle(p, msg)
    #                 .map(p -> p.handle(msg);
    results = list(map(lambda p: p.handle(msg), [p for p in plugins if canHandle(p, msg)]))
    if all(results):
        # archive
        print("ARCHIVE???")
        # server.delete_messages([uid])
    else:
        print("some plugin failed to process")

    # import ipdb; ipdb.set_trace()
server.logout()
