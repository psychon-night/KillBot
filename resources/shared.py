import dotenv
import os
import sys
import json

dotenv.load_dotenv(".env")

TOKEN = os.getenv("TOKEN")
PATH = sys.path[0]

CONFIG = json.loads(open(PATH + "/config.json", "r").read())
NUM_RESPONSES = len(CONFIG["death_messages"])

# Developer stuff
VERSION = "1.0"
DEBUG  = True
LOCKED = True