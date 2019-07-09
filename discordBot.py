import discord 
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from scapy.all import *
import sys
import datetime
import subprocess
import youtube_dl
import asyncio
import requests
import bs4
import random
from bs4 import BeautifulSoup

STATUS_DELAY = 1
BYTES_SIZE = 32
SEND_TIMES = 3
prefix = '#'


token = open("token.txt", "r").read()  # I've opted to just save my token to a text file. 

bot = commands.Bot('#')
bot.remove_command('help')

@bot.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by bot. This runs once when connected
    print(f'logged in as {bot.user}')  
    game = discord.Game("Minecraft")
    #await bot.change_presence(activity=game)

@bot.event
async def on_message(message):
	"""
	this function is an event :
	when a message is sent this function will be called
	"""
	all_traffic_channel = bot.get_channel(593823748852023352)

	if (message.channel != all_traffic_channel) and (message.author != bot.user):
		embed = discord.Embed(title="message", description=f"{message.content}" ,color=0x82b2ff)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="in channel",value = f"{message.channel}", inline=True)
		embed.add_field(name="by user:",value = f"{message.author}", inline=True)

		await all_traffic_channel.send(embed = embed)

	await bot.process_commands(message)


@bot.command(pass_context=True)
async def clear(ctx , number: int):
	"""
	this function handels the "clear" commmand 
	when the clear command is called the bot delete the given amout of msgs from the ctx channel
	"""

	all_traffic_channel = bot.get_channel(593823748852023352)
	await ctx.channel.purge(limit = number + 1)
	await all_traffic_channel.send(f"```\n\ncommand: {ctx.message.content} was used in channel: {ctx.channel}\nuser: {ctx.author}\nwith name: {ctx.author.name}```")


@clear.error
async def clear_error(ctx, error):
	"""
	this function handels what happes when a error occurs in the clear function
	"""
	if isinstance(error, discord.ext.commands.BadArgument):
		error_embed = discord.Embed(title="ERROR.", description="something went wrong" , color=0xFF0000)
		await ctx.channel.send(embed=error_embed)


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def ping(ctx , arg : str ):
	"""
	this function handels the "ping" commmand 
	when the ping command is called the bot using subprocess will ping the given ip and will send back the output
	"""
	embed = discord.Embed(title="ping info.", description="pinged {0} using the ping command".format(arg) ,color=0x00ff00)
	error_embed = discord.Embed(title="ping info.", description="pinged {0} using the ping command".format(arg) , color=0xFF0000)
	s = subprocess.check_output(["ping", arg])

	embed.add_field(name="raw data:", value= str(s.decode()) ,inline=True)
	await ctx.channel.send(embed=embed)


@ping.error
async def ping_error(ctx, error):
	"""
	this function hadels what happes when a error occurs in the ping function
	"""
	error_embed = discord.Embed(title="ERROR.", description=str(error) , color=0xFF0000)
	await ctx.channel.send(embed=error_embed)


@bot.command(pass_context=True)
async def echo(ctx , arg):
	"""
	this function handels the "echo" commmand 
	when the echo command is called the bot will send the recved arg back to the ctx user 
	"""
	await ctx.channel.send(arg)


@bot.command(pass_context=True)
async def join_voice(ctx):
	"""
	this function handels the "join_voice" commmand 
	when the join_voice command is called the bot will join the voice command that of the ctx user
	playing sound does not work 

	"""
	
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


@commands.is_owner()
@bot.command(pass_context=True)
async def quit(ctx):
	"""
	this function handels the "quit" commmand 
	when the quit command is called the bot will disconnet from discord and go offline
	"""
	await ctx.channel.send("bye!")
	await bot.close()

@quit.error
async def quit_error(ctx, error):
	"""
	this function handels what happes when a error occurs in the quit function
	"""
	error_embed = discord.Embed(title="ERROR.", description="{0}".format(error), color=0xFF0000)
	await ctx.channel.send(embed=error_embed)


@commands.is_owner()
@bot.command(pass_context=True)
async def cmd(ctx ,*, arg):
	"""
	this function handels the "cmd" commmand 
	when the cmd command is called the bot using subprocess the bot will do the given command in the host pc shell
	the user can give in the arg a cmd command and the bot will take it and run it
	"""
	embed = discord.Embed(title="command", description=str(arg) ,color=0x00ff00)
	print(arg)
	s = subprocess.check_output(arg , shell=True)

	embed.add_field(name="output", value= str(s.decode()) ,inline=True)
	await ctx.channel.send(embed=embed)

@cmd.error
async def cmd_error(ctx, error):
	"""
	this function handels what happes when a error occurs in the cmd function
	"""
	error_embed = discord.Embed(title="ERROR.", description="{0}".format(error), color=0xFF0000)
	await ctx.channel.send(embed=error_embed)


async def change_status():
	"""
	this function runs in a loop when the bot starts
	and will change the text that is displayed under the bot name in discord
	"""
	await bot.wait_until_ready()
	messages = ["h","he","hel","hell","hello" ,":D"]
	while bot.is_ready():
	    for msg in messages:
	        await bot.change_presence(activity=discord.Game(name=msg))
	        await asyncio.sleep(STATUS_DELAY)

@bot.command(pass_context= True)
async def theory(ctx):

	question_number = random.randint(1, 1500)

	url = "http://www.meteoria.co.il/repository/question/"+str(question_number)
	response = requests.get(url)
	



bot.loop.create_task(change_status())
bot.run(token)


