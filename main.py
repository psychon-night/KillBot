import asyncio
import nest_asyncio

import discord

from scripts.utils   import *
from scripts.killbot import *

from resources.shared import *
from resources.colour import *

# Vars # 
bot = discord.Bot()

# Patch event loop #
loop = asyncio.get_event_loop()
nest_asyncio.apply(loop)

@bot.event
async def on_ready():
	print(MAGENTA + f"{VERSION}\nConnected to Discord")
	dprint(RED + "Debug mode is enabled" + RESET)

	if LOCKED: print(RED + "Commands are currently locked to developers" + RESET)

# Register commands #
@bot.command(name='kill', description="Kill a user, but gently", pass_context=True)
async def _kill(ctx, target:discord.Option(discord.Member, description="User to target")): # type:ignore
	if (LOCKED) and (ctx.user.id != 1063584978081951814): return
	await kill_user(ctx, target, bot)

# Start the bot #
try:
	if os.path.isdir(f"{PATH}/.cache"):
		os.system(f"rm -r {PATH}/.cache")

	os.mkdir(f"{PATH}/.cache")

	bot.run(TOKEN)

except Exception as err:
	print(RED + "Failed to start!\n" + str(err) + RESET)