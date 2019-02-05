#!/usr/bin/python 

import json
import subprocess
import time

# bulkrejectgp script to be called
script = "./bulkrejectgp.py"

# load content from strings.json file
with open('strings.json') as f:
    file_content = json.load(f)

# extract lang and commands
opt_lang = file_content['lang']
commands = file_content['commands']

# extract single command
for command in commands:
    # get arguments
    opt_search = command['search']
    opt_remove = command['remove']
    if not command['replace']:
        cmd = subprocess.Popen([script,"--search",opt_search,"--remove",opt_remove,"--lang",opt_lang])
    else:
        opt_replace = command['replace']
        cmd = subprocess.Popen([script,"--search",opt_search,"--remove",opt_remove,"--replace",opt_replace,"--lang",opt_lang])
    # execute command
    cmd.communicate()
    # wait some time before next iteration, just to be sure
    time.sleep(5)
    print("--------------")
