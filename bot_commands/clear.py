import discord
from discord.ext import commands
RED = 0xFF0000


class clear_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def clear(self, ctx, number: int):
		"""
		this function handles the "clear" command
		when the clear command is called the bot delete the given amount of msgs from the ctx channel
		"""
		await ctx.channel.purge(limit=number + 1)

	@clear.error
	async def clear_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the clear function
		"""
		if isinstance(error, discord.ext.commands.BadArgument):
			error_embed = discord.Embed(title="ERROR.", description="something went wrong", color=RED)
			await ctx.channel.send(embed=error_embed)


def setup(bot):
	bot.add_cog(clear_command(bot))
