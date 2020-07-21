# Theory bot
# [Invite](https://discord.com/api/oauth2/authorize?client_id=624613109922791424&permissions=8&scope=bot)
A nice python bot for the Israeli theory test

This repo is a Linux version of the [original](https://github.com/YakirOren/theory-bot) discord bot repo


Commands can be changed and loaded by changing the BOT_COMMANDS list
```py
BOT_COMMANDS = [
	'clear',
	'ping',
	'cmd',
	'quit',
	'voice',
	'echo',
	'theory',
]
```


## Main Commands:
 :warning: being rewritin in newer versions.
  - theory:
    - Will send a theory question to the channel by default will have 25 seconds delay(this number can be changed).
      the user by default will have 240 seconds to answer (this number can be changed).
      
    - Permissions: Everyone.

   - theory_test:
      - Will send a theory question to the channel by default will have 25 seconds delay(this number can be changed).
        the user by default will have 240 seconds to answer (this number can be changed).
        
        after the user have answered the bot will send another question to the channel.
      - Parameters: number of questions.
      - Permissions: Everyone.


# :wrench: Tools
besides the main commands the bot has some other helpful commands:

- clear:
  - Clears the given numbers of messages in the channel.
  - Parameters: Amount of messages to delete.
  - Permissions: Everyone.

- echo:
   - Echoes back the given string.
   - Parameters: A string to echo.
   - Permissions: Everyone.

- ping:
  - Will ping the given address, the default is 1 ping per user with a 30 second delay.
  - Parameters: A domain/ IP to ping.
  - Permissions: Everyone.
  
# Admin commands: 

- cmd:
  - Will run the given command in a shell and send back the results.
  - Parameters: A command(With parameters or not) to run.
  - Permissions: Bot owner.
  
- quit:
  - Will close the bot.
  - Parameters: None.
  - Permissions: Bot owner.

# Voice channel commands:
 :warning: NOT FULLY IMPLEMNTED 
  - join:
    - Description: Will make the bot join the channel your currently in.
    - Parameters: None.
    - Permissions: Everyone.
