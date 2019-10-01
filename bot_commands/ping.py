import discord
from discord.ext import commands
import subprocess
RED = 0xFF0000
GREEN = 0x00FF00
COMMAND_DELAY = 30
NUMBER_OF_TIMES = 1  # The number of time a user can ping in the delay time.


class ping_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.cooldown(NUMBER_OF_TIMES, COMMAND_DELAY, commands.BucketType.user)
	async def ping(self, ctx, arg: str):
		"""
		this function handles the "ping" command
		when the ping command is called the bot using subprocess will ping the given IP and will send back the output
		"""
		embed = discord.Embed(title="ping info.", description="pinged {0} using the ping command".format(arg), color=GREEN)
		s = subprocess.check_output(["ping", arg])

		embed.add_field(name="raw data:", value=str(s.decode()), inline=True)
		await ctx.channel.send(embed=embed)

	@ping.error
	async def ping_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the ping function
		"""
		error_embed = discord.Embed(title="ERROR.", description=str(error), color=RED)
		await ctx.channel.send(embed=error_embed)


def setup(bot):
	bot.add_cog(ping_command(bot))
