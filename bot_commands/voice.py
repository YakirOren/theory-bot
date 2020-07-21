import discord
from discord.ext import commands
from discord.utils import get
RED = 0xFF0000


class voice_commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def join(self, ctx):
		"""
		this function handles the "join" command when the join command is
		called the bot will join the voice command that of the ctx user playing sound does not work
		"""
		channel = ctx.message.author.voice.channel
		if not channel:
			await ctx.send("You are not connected to a voice channel")
			return
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()

	@join.error
	async def join_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the join function
		"""
		error_embed = discord.Embed(title="ERROR.", description=str(error), color=RED)
		await ctx.channel.send(embed=error_embed)


def setup(bot):
	bot.add_cog(voice_commands(bot))
