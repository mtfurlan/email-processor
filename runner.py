#!/usr/bin/env python3

import os
import sys
import email
import email.policy
from dotenv import load_dotenv
from imapclient import IMAPClient
import importlib.util
from PluginABC import PluginABC
import glob
import re
import builtins
from inspect import getmembers, isclass

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
    module = import_from_path(f.replace(".py", "").replace("plugins/", "plugins."), f)
    p = [m[1] for m in getmembers(module, isclass) if m[1] in PluginABC.__subclasses__()]
    if not p:
        raise Exception(f"{f} contained no instances of PluginABC")
    plugins += list(map(lambda foo: foo(), p))


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

    # sender might be something like '"Victoria Scott (via Patreon)" <bingo@patreon.com>'
    # we want to filter on the email portion
    msg.senderRaw = re.findall(r'^(?:".*" )?<?(.*?)>?$', (msg.get("X-Google-Original-From") or msg.get("From")))[0]

    handled = False

    pluginsToRun = [p for p in plugins if p.canHandle(uid, msg)]

    printWidth = max([len(str(p)) for p in pluginsToRun])
    results = []
    for p in pluginsToRun:
        originalPrint = print
        # TODO: logging module
        def modulePrint(*objs, **kwargs):
            originalPrint(f"{p:<{printWidth}} > ", *objs, **kwargs)
        builtins.print = modulePrint
        result = False
        import traceback
        try:
            result = p.handle(uid, msg)
        except Exception as e:
            builtins.print = originalPrint
            print(f"plugin {p} had some issues, marking it failed and continuing")
            traceback.print_exception(e)
            result = False
        builtins.print = originalPrint
        results.append(result)

    if all(results):
        # archive
        print("ARCHIVE???")
        # server.delete_messages([uid])
    else:
        print("some plugin failed to process")
        print("\n".join([f"* {plugins[i]}" for i,v in enumerate(results) if not v]))

server.logout()
