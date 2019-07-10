import discord
from discord.ext import commands
RED = 0xFF0000


class echo_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def echo(self, ctx, arg):
		"""
		this function handles the "echo" command
		when the echo command is called the bot will send the received arg back to the ctx user
		"""
		await ctx.channel.send(arg)

	@echo.error
	async def echo_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the echo function
		"""
		error_embed = discord.Embed(title="ERROR.", description=str(error), color=RED)
		await ctx.channel.send(embed=error_embed)


def setup(bot):
	bot.add_cog(echo_command(bot))
