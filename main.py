# Imports
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os

# Discord Bot setup...
bot = commands.Bot(command_prefix="rpg.")

# Grab Token and Guild...
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Attempt to connect to a server...
print('Attempting to connect to', GUILD, 'using token', TOKEN)

# Show we connected once we did...
@bot.event
async def on_ready():
  for guild in bot.guilds:
    if guild.name == GUILD:
      break
  print('\nSuccessfully connected!\n')

@bot.command(name='test')
async def test(ctx):
  choices=['TESTING', 'HELLO', 'IM HERE NOW']
  response = random.choice(choices)
  await ctx.send(response)
  print(response)

bot.run(TOKEN)