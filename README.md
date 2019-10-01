# Theory bot
A nice python bot for the Israeli theory test

this repo is a linux version of the orignal discord bot repo 
https://github.com/YakirOren/theory-bot

## Commands:
- clear:
  - Description: Clears the given numbers of messages in the channel.
  - Parameters: Amount of messages to delete.
  - Permissions: Everyone.

- echo:
  - Description: Echos back the given string.
  - Parameters: A string to echo.
  - Permissions: Everyone.

- cmd:
  - Description: Will run the given command in a cmd and will send the results.
  - Parameters: A command(With parameters or not) to run.
  - Permissions: Bot owner.

- ping:
  - Description: Will ping the given address, the default is 1 ping per user with a 30 second delay.
  - Parameters: A domain/ IP to ping.
  - Permissions: Everyone.

- quit:
  - Description: Will close the bot.
  - Parameters: None.
  - Permissions: Bot owner.
  
- Voice channel commands:
  - join:
    - Description: Will make the bot join the channel your currently in.
    - Parameters: None.
    - Permissions: Everyone.

- Theory commands:
  - theory:
    - Description: Will send a theory question to the channel by default will have 25 seconds delay(this number can be changed).
      the user by default will have 240 seconds to answer (this number can be changed).
    - Parameters: None.
    - Permissions: Everyone.
    
   - theory_test:
    - Description: Will send a theory question to the channel by default will have 25 seconds delay(this number can be changed).
      the user by default will have 240 seconds to answer (this number can be changed).
      after the user have answerd the bot will send another question to the channel.
    - Parameters: number of questions.
    - Permissions: Everyone.
    
