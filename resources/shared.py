import dotenv
import os
import sys
import json
import random

dotenv.load_dotenv(".env")

TOKEN = os.getenv("TOKEN")
PATH = sys.path[0]

CONFIG = json.loads(open(PATH + "/config.json", "r").read())
NUM_RESPONSES = len(CONFIG["death_messages"])

_rid__te = ""
_rid__le = []

for i in range(0,64):
	_rid__le.append(random.randint(0,9))

for char in _rid__le:
	_rid__te = _rid__te + str(char)

RUN_ID = _rid__te

del _rid__te
del _rid__le

# Developer stuff
VERSION = "1.4.0"
DEBUG  = True
LOCKED = False