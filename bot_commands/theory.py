import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
import re
TIME_TO_ANSWER = 60.0
THEORY_URL = "http://www.meteoria.co.il/repository/question/"

GREEN = 0x00ff00
RED = 0xFF0000

# Emojis
THUMBS_UP_EMOJI = '👍'
THUMBS_DOWN_EMOJI = '👎'
ONE_EMOJI = '1⃣'
TWO_EMOJI = '2⃣'
THREE_EMOJI = '3⃣'
FOUR_EMOJI = '4⃣'


class theory_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def theory(self, ctx):
		answer_number = 0
		correct_answer = 0
		question_number = random.randint(1, 1500)
		url = THEORY_URL + str(question_number)

		async with aiohttp.ClientSession() as session:
			html = await self.fetch(session, url)
			soup = BeautifulSoup(html, "html.parser")

			question = soup.findAll('h1')
			question = re.findall("<h1>.+</h1>", str(question))[0][4:-5]
			embed = discord.Embed(title=question, description="", color=GREEN)

			for i in soup.findAll('li')[-4:]:
				answer_number += 1
				if 'data-corrent="1"' in str(i):
					correct_answer = answer_number
				embed.add_field(name=answer_number, value=re.findall("<span>.+</span>", str(i))[0][6:-7] + "\n", inline=True)
			msg = await ctx.channel.send(embed=embed)

			await msg.add_reaction(ONE_EMOJI)
			await msg.add_reaction(TWO_EMOJI)
			await msg.add_reaction(THREE_EMOJI)
			await msg.add_reaction(FOUR_EMOJI)

			try:
				reaction, user = await self.bot.wait_for(
					'reaction_add',
					timeout=TIME_TO_ANSWER,
					check=lambda user, reaction: user == ctx.author and str(reaction.emoji) == THUMBS_UP_EMOJI
				)
			except asyncio.TimeoutError:
				await ctx.channel.send(THUMBS_DOWN_EMOJI)
			else:
				await ctx.channel.send('😉')

	@theory.error
	async def theory_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the theory function
		"""
		error_embed = discord.Embed(title="ERROR.", description=str(error), color=RED)
		await ctx.channel.send(embed=error_embed)

	async def fetch(self, session, url):
		async with session.get(url) as response:
			return await response.text()


def setup(bot):
	bot.add_cog(theory_command(bot))
