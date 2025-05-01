import datetime
import random
import discord

from discord.ext import tasks # This is not unused, do not remove!

from resources.shared import *
from scripts.utils    import *

TOTAL_COOLDOWN_TIME_SECONDS = CONFIG["timeout_seconds"] + CONFIG["cooldown_seconds"]

def check_user(id:int) -> list:
	""" Check whether the user is timed out already and whether they're excluded """

	timed_out = False
	excluded = False

	if os.path.exists(f"{PATH}/.cache/{id}"): timed_out = True
	if id in CONFIG["excluded_users"]: excluded = True

	return timed_out, excluded

def set_timeout(id, bot:discord.Bot):
	current_time = discord.utils.generate_snowflake()
	end_timeout  = current_time + (CONFIG["timeout_seconds"]*1000)
	end_cooldown = end_timeout  + (CONFIG["cooldown_seconds"]*1000)

	dprint(f"CT: {current_time}, ET: {end_timeout}. EC: {end_cooldown}")

	# Set events
	funcs = f"""@tasks.loop(seconds=CONFIG["timeout_seconds"], count=1)
async def end_timeout_{id}():
	NotImplemented

@end_timeout_{id}.after_loop
async def et_end_{id}():
	dprint(f"Timeout ended for {id}")

@tasks.loop(seconds=TOTAL_COOLDOWN_TIME_SECONDS, count=1)
async def end_cooldown_{id}():
	NotImplemented

@end_timeout_{id}.after_loop
async def ec_end_{id}():
	dprint(f"Ending cooldown for {id}")
	os.remove(f"{PATH}/.cache/{id}")
"""

	exec(compile(funcs, f"funcs_{id}", "exec"))
	exec(compile(f"end_timeout_{id}.start()", f"et_start_{id}", "exec"))
	exec(compile(f"end_cooldown_{id}.start()", f"ec_start_{id}", "exec"))

	return end_timeout

async def kill_user(ctx, user:discord.Member, bot:discord.Bot):
	await ctx.defer()

	origin = bot.get_user(ctx.author.id)
	name   = user.display_name
	id     = user.id

	dprint(f"Got request to kill {name}, uid {id}")

	timed_out, excluded = check_user(id)

	dprint(f"{name} timed out: {MAGENTA}{timed_out}")
	dprint(f"{name} excluded:  {MAGENTA}{excluded}")

	match [timed_out, excluded]:
		case [True, _]:
			dprint(f"{RED}{name} is timed out. Will not kill")

			await ctx.respond(f"{name} is already dead or on cooldown!")

		case [_, True]:
			dprint(f"{RED}{name} is excluded. Will not kill")

			await ctx.respond(f"{name} cannot be killed")

		case [False, False]:
			dprint(f"{SPECIALDRIVE}{name} will be killed")

			open(f"{PATH}/.cache/{id}", "x").close() # Create the cache file
			
			set_timeout(id, bot)
			
			try: 
				await user.timeout_for(datetime.timedelta(seconds=CONFIG["timeout_seconds"]))
			
			except Exception as err:
				dprint("Failed to kill user: " + str(err))

				if "Missing Permissions" in str(err):
					await ctx.respond("Cannot possibly kill user, they're above me in the permissions list")
					dprint("Likely because this user is the server owner, or bot is misconfigured on the server itself")

				else:
					await ctx.respond("Failed to kill this user")

				return

			try:
				kill_message = CONFIG["death_messages"][random.randint(0, NUM_RESPONSES-1)]

				# await ctx.respond(f"debug: {name} ({id}) to be killed")
				await ctx.respond(kill_message%(origin.display_name, name))

			except Exception as err:
				dprint("Failed to send fun death message! " + str(err))

				await ctx.respond(CONFIG["generic_death_message"]%(name))
