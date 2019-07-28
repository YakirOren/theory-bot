import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient

COMMANDS_FOLDER = "bot_commands"  # Don't add slash in the end
BOT_COMMANDS = [
	'clear',
	'ping',
	'cmd',
	'quit',
	'voice',
	'echo',
	'theory',
]

STATUS_DELAY = 1
STATUS_MESSAGES = ["h", "he", "hel", "hell", "hello", ":D"]

PREFIX = '#'
TOKEN_FILE = "token.txt"
TOKEN = open(TOKEN_FILE, "r").read()  # I've opted to just save my token to a text file
LIGHT_BLUE = 0x82b2ff

CONSOLE_CHANNEL_ID = 593823748852023352

bot = commands.Bot(PREFIX)
bot.remove_command('help')

# Database options, this is using MongoDB
USE_DATABASE = False
link_to_connection = 'mongodb://localhost:27017'
database_name = 'bot'
collection_name = 'moderation'
client = MongoClient(link_to_connection)
db = client[database_name]
collection = db[collection_name]


@bot.event
async def on_ready():
	print(f'logged in as {bot.user}')
	if USE_DATABASE:
		print('Inserting data to DB, this may take some time...')
		channels = []
		for channel in bot.get_all_channels():
			if str(channel.type) == 'text':
				msg = await channel.history(limit=1).flatten()
				if not collection.find_one({'channel_id': str(channel.id)}):
					last_msg = ''
					if len(msg) > 0:
						last_msg = {
							'content': str(msg[0].content),
							'author': str(msg[0].author),
							'author_id': str(msg[0].author.id),
							'msg_time': str(msg[0].created_at),
						}
					channels.append({
						'channel_id': str(channel.id),
						'server_name': str(channel.guild),
						'channel_name': str(channel.name),
						'last_msg': last_msg
					})
		if len(channels) > 0:
			collection.insert_many(channels)
		print('Finished inserting to the DB!')
	# game = discord.Game("Minecraft")
	# await bot.change_presence(activity=game)


@bot.event
async def on_message(message):
	"""
	this function is an event :
	when a message is sent this function will be called
	"""
	invites = None
	all_traffic_channel = bot.get_channel(CONSOLE_CHANNEL_ID)

	if (message.channel != all_traffic_channel) and (message.author != bot.user):
		embed = discord.Embed(title="message", description=f"{message.content}", color=LIGHT_BLUE)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name="in channel", value=f"{message.channel}")
		embed.add_field(name="by user:", value=f"{message.author}")
		try:
			invites = ["https://discord.gg/" + "".join(invite.code) for invite in await message.channel.invites()]
		except Exception:
			pass

		embed.add_field(name="invite to guild: ", value=f"{invites}")
		await all_traffic_channel.send(embed=embed)

	await bot.process_commands(message)


async def change_status():
	"""
	this function runs in a loop when the bot starts
	and will change the text that is displayed under the bot name in discord
	"""
	await bot.wait_until_ready()
	while bot.is_ready():
		for msg in STATUS_MESSAGES:
			await bot.change_presence(activity=discord.Game(name=msg))
			await asyncio.sleep(STATUS_DELAY)


if __name__ == "__main__":
	for command in BOT_COMMANDS:
		try:
			bot.load_extension('.'.join([COMMANDS_FOLDER.replace('/', '.').replace('\\', '.'), command]))
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			print('Failed to load command {}\n{}'.format(command, exc))


bot.loop.create_task(change_status())
bot.run(TOKEN)
