import discord
from discord.ext import commands


class clear_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def clear(self, ctx , number: int):
		"""
		this function handels the "clear" commmand 
		when the clear command is called the bot delete the given amout of msgs from the ctx channel
		"""

		all_traffic_channel = self.bot.get_channel(593823748852023352)
		await ctx.channel.purge(limit = number + 1)
		await all_traffic_channel.send(f"```\n\ncommand: {ctx.message.content} was used in channel: {ctx.channel}\nuser: {ctx.author}\nwith name: {ctx.author.name}```")


	@clear.error
	async def clear_error(self, ctx, error):
		"""
		this function handels what happes when a error occurs in the clear function
		"""
		if isinstance(error, discord.ext.commands.BadArgument):
			error_embed = discord.Embed(title="ERROR.", description="something went wrong" , color=0xFF0000)
			await ctx.channel.send(embed=error_embed)


def setup(bot):
    bot.add_cog(clear_command(bot))