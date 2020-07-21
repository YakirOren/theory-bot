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
QUESTION_URL = "http://www.meteoria.co.il/repository/question/"
IMG_URL = "htttp://www.meteoria.co.il/content/img/"



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



class Question():
       
    def __init__():
        
        #new question request to the server 
        
        # the server returns title, answers and image(optional)
        
        # make embed function?
        pass

    def create_embed():
        pass

    def send_to_chat():
        pass

    

    


class theory_command(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

        @commands.group()
        async def theory(self, ctx):
            #send a start game request
            # create a new Question obj
            pass

        @theory.command()
        async def test(self, ctx):
            
            
            pass

        

def setup(bot):
	bot.add_cog(theory_command(bot))
