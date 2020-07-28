# Imports
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os
import users, arenas, shops
from formatname import formatter
from webserver import keep_alive
import asyncio

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

""" COMMANDS FOR P2P INTERACTION """

# Create a new player.
@bot.command(name='new', help="Create a new user. Format: <rpg.new ExampleClassName>")
async def new(ctx, *, clss):
    response = users.create_user(users.data, formatter(str(ctx.message.author)), clss)
    await ctx.send(response)

# Edit player class.
@bot.command(name='class', help="Change your class. Format: <rpg.class Class Name Example>")
async def clss(ctx, *, clss):
    response = users.change_class(users.data, formatter(str(ctx.message.author)), clss)
    await ctx.send(response)

# Check player class.
@bot.command(name='whatclass', help="Check what your current class is.")
async def whatclass(ctx):
    response = users.check_class(users.data, formatter(str(ctx.message.author)))
    await ctx.send(response)

# Check player inventory.
@bot.command(name='inv', help="Check your inventory.")
async def inv(ctx):
    lst = users.get_inventory(users.data, formatter(str(ctx.message.author)))
    response = ":scroll: **" + formatter(str(ctx.message.author)) + "'s INVENTORY** :scroll:"
    await ctx.send(response)
    response = "-" * len(response)
    await ctx.send(response)
    e=1
    for re in lst:
      r = str(e) + ". " + str(re)
      await ctx.send(r)
      e+=1

# Check player stats.
@bot.command(name='stats', help="Check your stats.")
async def stats(ctx):
    lst = users.check_stats(users.data, formatter(str(ctx.message.author)))
    response = ":crossed_swords: **" + formatter(str(ctx.message.author)) + "'s STATS** :crossed_swords:"
    await ctx.send(response)
    response = "-" * (len(response)-19)
    await ctx.send(response)
    e=1
    for re in lst:
      if e==1:
        r = ":scroll: " + str(re)
        await ctx.send(r)
      if e==2:
        r = ":green_book: " + str(re)
        await ctx.send(r)
      if e==3:
        r = ":heart: " + str(re)
        await ctx.send(r)
      e+=1

# Give another player an item.
@bot.command(name='give', help="Give an item. Format: <rpg.give TheirName ItemName ItemAmount>")
async def give(ctx, theirname, itemname, itemamount):
    response = users.give_item(users.data, formatter(str(ctx.message.author)), str(theirname), str(itemname), int(itemamount))
    await ctx.send(response)

# Give player item. (OP)
@bot.command(name='add', hidden=True, has_role="Admin")
@commands.has_role('Admin')
async def add_item(ctx, *, itemname):
    response = users.give_player_item(users.data, formatter(str(ctx.message.author)), str(itemname), 1)
    await ctx.send(response)

# Consume item.
@bot.command(name='consume', help="Consume an item. Format: <rpg.consume ItemName>")
async def consume(ctx, *, itemname):
    response = users.consume_item(users.data, formatter(str(ctx.message.author)), itemname)
    await ctx.send(response)

# Check shop.
@bot.command(name='shop', help="Consume an item.")
async def shop(ctx):
    response = shops.check_shop(shops.data)
    await ctx.send(response)


"""COMMANDS FOR BOSSFIGHTS"""
# Start fight
@bot.command(name='approach', help="Begin a boss fight.")
async def start_fight(ctx):
    response = arenas.start_fight(users.data, formatter(str(ctx.message.author)))
    await ctx.send(response)

# Attack boss...
@bot.command(name='attack', help="Begin a boss fight.")
async def deal_damage(ctx):
    response = arenas.damage_boss(users.data, formatter(str(ctx.message.author)))
    await ctx.send(response)

keep_alive()
bot.run(TOKEN)
