import asyncio
import nest_asyncio
import copy

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
	print(MAGENTA + f"Connected to Discord")

	if LOCKED: 
		print(RED + "Commands are currently locked to developers" + RESET)

# Register commands #
@bot.command(name='run_id', description="Gets the current RUN_ID", pass_context=True)
async def _getrunid(ctx):
	await ctx.respond(str(RUN_ID), ephemeral=True)

@bot.command(name='kill', description="Kill a user, but gently", pass_context=True)
async def _kill(ctx, target:discord.Option(discord.Member, description="User to target")): # type:ignore
	if (LOCKED) and (ctx.user.id != 1063584978081951814): return
	await kill_user(ctx, target, bot)

@bot.command(name='overwrite_times', description="Overwrites timeout or cooldown length, in seconds. Restarts bot!")
async def _set_timeout(ctx, mode:discord.Option(str, choices=["Timeout", "Cooldown"], description="Which object to overwrite"), time_secs:discord.Option(int, description="Number of seconds for timeout")): #type:ignore
	await ctx.defer()

	if not ctx.author.id in CONFIG["developers"]:
		await ctx.respond("You may not change this parameter")
		return

	CONFIG_SNAPSHOT = copy.deepcopy(CONFIG)
	dumped = False
	
	if mode == "Timeout":
		CONFIG["timeout_seconds"] = time_secs
		response = f"Timeout length set to {time_secs} seconds"

	elif mode == "Timeout":
		CONFIG["cooldown_seconds"] = time_secs
		response = f"Cooldown length set to {time_secs} seconds"

	try:
		with open(f"{PATH}/config.json", "w") as config_file:
			config_file.truncate(0)

			config_file.write(json.dumps(CONFIG, indent=4))
			config_file.close()

	except Exception as err:
		dprint(RED + "FATAL! FATAL! FATAL! CONFIG MAY BE TRUNCATED!")
		dprint(str(err))
		response = "Failed to overwrite value. Verify config integrity!"

		panic_config_dump(json.dumps(CONFIG_SNAPSHOT, indent=4))
		dumped = True

	await ctx.respond(response)

	if not dumped:
		dprint(f"Restarting to apply config changes, as requested by {ctx.author.id}")

		if os.getlogin() == "fritz":
			os.system("sudo systemctl restart killbot")
		else:
			dprint(RED + "Manual restart is required!")

# Start the bot #
try:
	if os.path.isdir(f"{PATH}/.cache"):
		os.system(f"rm -r {PATH}/.cache")

	os.mkdir(f"{PATH}/.cache")

	if not os.path.isdir(f"{PATH}/logs"):
		os.mkdir(f"{PATH}/logs")

	print(MAGENTA + f"KillBot {VERSION}" + RESET)
	dprint(RED + "Debug mode is enabled" + RESET)
	
	dprint(f"Loaded {len(CONFIG["developers"])} developers: {CONFIG["developers"]}")
	dprint(f"Loaded exclusion list: {CONFIG["excluded_users"]}")
	dprint(f"Loaded {len(CONFIG["death_messages"])} responses")

	bot.run(TOKEN)

except Exception as err:
	print(RED + "Failed to start!\n" + str(err) + RESET)