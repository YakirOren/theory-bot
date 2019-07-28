import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
import re
TIME_TO_ANSWER = 240.0
THEORY_URL = "http://www.meteoria.co.il/repository/question/"

GREEN = 0x00ff00
RED = 0xFF0000
PURPLE = 0xcc0acc

# Emojis
THUMBS_UP_EMOJI = '👍'
THUMBS_DOWN_EMOJI = '👎'
ONE_EMOJI = '1⃣'
TWO_EMOJI = '2⃣'
THREE_EMOJI = '3⃣'
FOUR_EMOJI = '4⃣'

ANSWER_DICT = {ONE_EMOJI: 1, TWO_EMOJI: 2, THREE_EMOJI: 3, FOUR_EMOJI: 4}

theory_msg = None


class theory_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def make_question(self, ctx, score_embed=None, mode=None):
		global theory_msg
		answer_number = 0
		correct_answer = 0
		question_number = random.randint(1, 900)

		question_image_url = "http://www.meteoria.co.il/Content/img/" + str(question_number) + ".jpg"
		url = THEORY_URL + str(question_number)

		async with aiohttp.ClientSession() as session:
			html = await self.fetch(session, url)
			soup = BeautifulSoup(html, "html.parser")

			question = soup.findAll('h1')
			question = re.findall("<h1>.+</h1>", str(question))[0][4:-5]
			embed = discord.Embed(title=question, description="", color=GREEN)
			try:
				embed.set_image(url=question_image_url)
			except Exception:
				pass
			embed.set_footer(text=f"שאלה מספר {question_number}")
			for i in soup.findAll('li')[-4:]:
				answer_number += 1
				if 'data-corrent="1"' in str(i):
					correct_answer = answer_number
				embed.add_field(name=answer_number, value=re.findall("<span>.+</span>", str(i))[0][6:-7] + "\n")

			if theory_msg is None:
				msg = await ctx.channel.send(embed=embed)
				theory_msg = msg
			else:
				msg = theory_msg
				await msg.edit(embed=embed)
				await msg.clear_reactions()

			await msg.add_reaction(ONE_EMOJI)
			await msg.add_reaction(TWO_EMOJI)
			await msg.add_reaction(THREE_EMOJI)
			await msg.add_reaction(FOUR_EMOJI)

			try:
				reaction, user = await self.bot.wait_for(
					'reaction_add',
					timeout=TIME_TO_ANSWER,
					check=lambda reaction, user: user is ctx.author and str(reaction) in ANSWER_DICT.keys()
				)
			except asyncio.TimeoutError:
				await ctx.channel.send(THUMBS_DOWN_EMOJI)
			else:
				try:
					if ANSWER_DICT[str(reaction)] == correct_answer:
						if mode != "test":
							await ctx.channel.send('correct answer!')
						else:
							return (1, score_embed)
					else:
						if mode != "test":
							await ctx.channel.send(f'wrong answer! the correct answer is {correct_answer}')
						else:
							score_embed.add_field(name=question, value=f"the correct answer is {correct_answer} you have answered {ANSWER_DICT[str(reaction)]}")
							return(0, score_embed)

				except Exception:
					pass

	async def fetch(self, session, url):
		async with session.get(url) as response:
			return await response.text()

	@commands.command()
	async def theory_test(self, ctx, number_of_questions: int):
		number_of_questions = abs(number_of_questions)
		global theory_msg
		theory_msg = None
		points = 0
		score_embed = discord.Embed(title="score", description=None, color=PURPLE)
		for question in range(number_of_questions):
			try:
				returned = await self.make_question(ctx, score_embed=score_embed, mode="test")
				points += returned[0]
				score_embed = returned[1]
			except Exception as e:
				print(e)

		await theory_msg.delete()
		score_embed.add_field(name="correct", value=f"you answered correct on {points} / {number_of_questions}")
		await ctx.channel.send(embed=score_embed)

	@commands.command()
	async def theory(self, ctx):
		global theory_msg
		theory_msg = None
		await self.make_question(ctx)

	@theory_test.error
	@theory.error
	async def question_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the theory function
		"""
		error_embed = discord.Embed(title="ERROR.", description=str(error), color=RED)
		await ctx.channel.send(embed=error_embed)


def setup(bot):
	bot.add_cog(theory_command(bot))
