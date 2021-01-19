import discord
import random
import json
from discord.ext import commands
from api import api_key
import time


client = commands.Bot(command_prefix='login ')

f = open('fortune.json', "r")
data = json.loads(f.read())
print(type(data))
# print(data)
print(len(data))

# print(api_key)

@client.event
async def on_ready():
    print('Bot is ready.')

# @client.event
# async def on_member_join(member):
    # print(f'{member} has joined a server.')

# @client.event
# async def on_member_remove(member):
    # print(f'{member} has left a server.')
@client.command()
async def fortune(ctx):
    index = random.randint(0,356)
    print(index)
    fortune = data[index].get('fortune')
    print(data[index].get('fortune'))
    await ctx.send(f"Today's fortune: {fortune}")

@client.command()
async def future(ctx):
    print("I see darkness inside you")
    await ctx.send("I see darkness inside you")
    time.sleep(3)
    print("Oh... My bad. It's your poop")
    await ctx.send("Oh... My bad. It's your poop")


client.run(api_key)
