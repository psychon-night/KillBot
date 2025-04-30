from resources.shared import *
from resources.colour import *

def dprint(string:str):
	""" Prints in debug mode, does nothing otherwise """

	if DEBUG:
		print(f"{MAGENTA}[DEBUG]{YELLOW} {string}{RESET}")

	