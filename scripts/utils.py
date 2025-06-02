from resources.shared import *
from resources.colour import *
import time

def current_milli_time():
    return round(time.time() * 1000)

def dprint(string:str):
	""" Prints in debug mode, does nothing otherwise """

	if DEBUG:
		print(f"{MAGENTA}[DEBUG]{YELLOW} {string}{RESET}")

		if not os.path.exists(f"{PATH}/logs/{RUN_ID}.log"):
			open(f"{PATH}/logs/{RUN_ID}.log", "x").close()

		with open(f"{PATH}/logs/{RUN_ID}.log", "a") as logfile:
			logfile.write(dstrip(string + "\n"))

def dlog(string:str):
	if not os.path.exists(f"{PATH}/logs/{RUN_ID}.log"):
		open(f"{PATH}/logs/{RUN_ID}.log", "x").close()

		with open(f"{PATH}/logs/{RUN_ID}.log", "a") as logfile:
			logfile.write(dstrip(string + "\n"))

def panic_config_dump(config:str):
	with open(f"{PATH}/crash_{RUN_ID}", "x") as logfile:
		logfile.write(config)

def dstrip(string:str) -> str:
	return string.replace(RED, "").replace(YELLOW, "").replace(BLUE, "").replace(SPECIALDRIVE, "").replace(MAGENTA, "").replace(DRIVES, "").replace(SEAFOAM, "")
