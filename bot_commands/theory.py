import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
import re
import pickle
import os
import traceback

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

COMMAND_DELAY = 25
NUMBER_OF_TIMES = 1  # The number of time a user can ping in the delay time.


class theory_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def make_question(self, ctx, score_embed=None, mode=None):
		"""
		This function will make a question and will send it to chat.
		First the function gets the question from the Meteoria data base,
		parses it and sends it to the ctx chat as an embed.

		This function also has an optional parameter called 'mode'
		this parameter changes the function behavior:

		When mode = 'test'
		the function will
		"""
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
				embed.add_field(name=answer_number, value=re.findall("<span>.+</span>", str(i))[0][6:-7] + "\n", inline=False)


			author_id = ctx.author.id
			if self.msg_file_exits(author_id) is False:
				msg = await ctx.channel.send(embed=embed)
				with open(str(author_id) + "msg_id.txt", 'w') as file:
					file.write(str(msg.id))
			else:
				with open(str(author_id) + "msg_id.txt", 'r') as file:
					msg_id = file.read()

					msg = await ctx.channel.fetch_message(int(msg_id))

				await msg.edit(embed=embed) # replacing the old message with our new one
				await msg.clear_reactions() # clearing the Emojis because the answer from the last question is still there and if we will not clear them its going to automaticly answer the new question with the old answer

			# adding the Emojis back after we cleared them, so the user can answer.
			await msg.add_reaction(ONE_EMOJI)
			await msg.add_reaction(TWO_EMOJI)
			await msg.add_reaction(THREE_EMOJI)
			await msg.add_reaction(FOUR_EMOJI)

			try:
				# when a reaction is added the bot will check if the added reaction is from the user who reqested the test
				reaction, user = await self.bot.wait_for(
					'reaction_add',
					timeout=TIME_TO_ANSWER,
					check=lambda reaction, user: user is ctx.author and str(reaction) in ANSWER_DICT.keys() # the bot also checks if the reaction added is the from our ANSWER_DICT
				)
			except asyncio.TimeoutError: # if the time has run out the bot will send a THUMBS_DOWN_EMOJI.
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
							score_embed.add_field(name=question, value=f"the correct answer is {correct_answer} you have answered {ANSWER_DICT[str(reaction)]}", inline=False)
							return(0, score_embed)

				except Exception:
					pass

	async def fetch(self, session, url):
		async with session.get(url) as response:
			return await response.text()

	def is_dm_channel(self, ctx):
		return ctx.message.guild is not None

	def msg_file_exits(self, author_id):
		try:
			f = open(str(author_id) + "msg_id.txt")
			f.close()
			return True
		except Exception:
			return False

	def delete_msg_file(self, ctx):
		author_id = ctx.author.id
		if self.msg_file_exits(author_id):
			os.remove(str(author_id) + "msg_id.txt") # deleting the file with the id of the message

	@commands.command()
	@commands.cooldown(NUMBER_OF_TIMES, COMMAND_DELAY, commands.BucketType.user)
	async def theory_test(self, ctx, number_of_questions: int):
		author_id = ctx.author.id

		self.delete_msg_file(ctx)

		number_of_questions = abs(number_of_questions)
		if number_of_questions > 30:
			raise ValueError("number is too big")
		points = 0
		score_embed = discord.Embed(title=str(ctx.author) +"\'s score", description=None, color=PURPLE, inline=False)
		for question in range(number_of_questions):
			try:
				returned = await self.make_question(ctx, score_embed=score_embed, mode="test")
				points += returned[0]
				score_embed = returned[1]
			except Exception as e:
				print(e)

		score_embed.add_field(name="correct", value=f"{str(ctx.author)} answered correct on {points} / {number_of_questions}", inline=False)

		if self.msg_file_exits(author_id):
			with open(str(author_id) + "msg_id.txt", 'r') as file:
				msg_id = file.read()
			msg = await ctx.channel.fetch_message(int(msg_id))
			await msg.edit(embed=score_embed)
			await msg.clear_reactions()

			self.delete_msg_file(ctx)
		else:
			await ctx.channel.send(embed=score_embed)

	@commands.command()
	@commands.cooldown(NUMBER_OF_TIMES, COMMAND_DELAY, commands.BucketType.user)
	async def theory(self, ctx):
		"""
		"""
		self.delete_msg_file(ctx)
		await self.make_question(ctx)
		self.delete_msg_file(ctx)

	@theory_test.error
	@theory.error
	async def question_error(self, ctx, error):
		"""
		this function handles what happens when a error occurs in the theory function
		"""
		error_embed = discord.Embed(title="ERROR.", description=str(error), color=RED)
		await ctx.channel.send(embed=error_embed)

		if isinstance(ctx, commands.CommandInvokeError):
			self.delete_msg_file(ctx)
			traceback_error_embed = discord.Embed(title="ERROR.", description=traceback.format_exc(), color=RED)
			await ctx.channel.send(embed=traceback_error_embed)

		# if isinstance(ctx, commands.CommandOnCooldown()):




def setup(bot):
	bot.add_cog(theory_command(bot))
