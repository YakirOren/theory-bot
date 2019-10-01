import discord
from discord.ext import commands
import subprocess
RED = 0xFF0000
GREEN = 0x00ff00

CMD_USERS = ["yakirLaptop#4906", "YakirOren#1424"]


class cmd_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def is_cmd_user(ctx):
		return str(ctx.author) in CMD_USERS

	@commands.check(is_cmd_user)
	@commands.command(pass_context=True)
	async def cmd(self, ctx, *, arg):
		"""
		this function handles the "cmd" command
		when the cmd command is called the bot using subprocess the bot will do the given command in the host pc shell
		the user can give in the arg a cmd command and the bot will take it and run it
		"""
		embed = discord.Embed(title="command", description=str(arg), color=GREEN)
		try:
			s = subprocess.check_output(arg, shell=True)
			embed.add_field(name="output", value=str(s.decode()), inline=True)
		except Exception:
			pass
		await ctx.channel.send(embed=embed)

	@cmd.error
	async def cmd_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the cmd function
		"""
		error_embed = discord.Embed(title="ERROR.", description="{0}".format(error), color=RED)
		await ctx.channel.send(embed=error_embed)


def setup(bot):
	bot.add_cog(cmd_command(bot))
