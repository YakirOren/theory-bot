import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
import re
import pickle
import os
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

theory_file_exist = False  # checks if the pickle file for this user exist
COMMAND_DELAY = 25
NUMBER_OF_TIMES = 1  # The number of time a user can ping in the delay time.


class theory_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def make_question(self, ctx, score_embed=None, mode=None):
		global theory_file_exist
		answer_number = 0
		correct_answer = 0
		question_number = random.randint(1, 900)

		question_image_url = "http://www.meteoria.co.il/Content/img/" + str(question_number) + ".jpg"  # we are using meteoria question bank for this bot
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

			try:
				f = open(ctx.author + "theory_file.pickle")
				f.close()
			except Exception:
				theory_file_exist = False

			if theory_file_exist is False:
				msg = await ctx.channel.send(embed=embed)
				with open(ctx.author + "theory_file.pickle", 'wb') as file:
					pickle.dump(msg, file)

				theory_file_exist = True
			else:
				with open(ctx.author + "theory_file.pickle", 'rb') as file:
					msg = pickle.load(file)
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

	def is_dm_channel(self, ctx):
		return ctx.message.guild is not None

	@commands.check(is_dm_channel)
	@commands.command()
	@commands.cooldown(NUMBER_OF_TIMES, COMMAND_DELAY, commands.BucketType.user)
	async def theory_test(self, ctx, number_of_questions: int):
		number_of_questions = abs(number_of_questions)
		global theory_file_exist
		theory_file_exist = False
		points = 0
		score_embed = discord.Embed(title="score", description=None, color=PURPLE)
		for question in range(number_of_questions):
			try:
				returned = await self.make_question(ctx, score_embed=score_embed, mode="test")
				points += returned[0]
				score_embed = returned[1]
			except Exception as e:
				print(e)

		with open(ctx.author + "theory_file.pickle", 'rb') as file:  # reading from the pickle file the question embed
			await pickle.load(file).delete()
			os.remove("theory_file.pickle")

		score_embed.add_field(name="correct", value=f"you answered correct on {points} / {number_of_questions}")
		await ctx.channel.send(embed=score_embed)

	@commands.command()
	@commands.cooldown(NUMBER_OF_TIMES, COMMAND_DELAY, commands.BucketType.user)
	async def theory(self, ctx):
		"""
		"""
		global theory_file_exist
		theory_file_exist = False
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
