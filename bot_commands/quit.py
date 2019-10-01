import discord
from discord.ext import commands
RED = 0xFF0000


class quit_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.is_owner()
	@commands.command(pass_context=True)
	async def quit(self, ctx):
		"""
		this function handles the "quit" command
		when the quit command is called the bot will disconnect from discord and go offline
		"""
		await ctx.channel.send("bye!")
		await self.bot.close()

	@quit.error
	async def quit_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the quit function
		"""
		error_embed = discord.Embed(title="ERROR.", description="{0}".format(error), color=RED)
		await ctx.channel.send(embed=error_embed)


def setup(bot):
	bot.add_cog(quit_command(bot))