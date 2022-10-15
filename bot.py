import discord
import random
import json
from discord.ext import commands
from api import api_key
import time
import os
import schedule

humanList = []

client = commands.Bot(command_prefix='login ')

# path = os.getcwd()
# dirName = os.path.dirname(path) + '/fortune.json'
dirName = os.getcwd() + '/fortune.json'

print(dirName)

f = open(dirName, "r")
data = json.loads(f.read())
print(type(data))
# print(data)
print(len(data))

# print(api_key)

def clear_human():
    humanList.clear()

schedule.every().day.at("00:00").do(clear_human)


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
    if ctx.author.name not in humanList:
        index = random.randint(0,356)
        print(index)
        fortune = data[index].get('fortune')
        print(data[index].get('fortune'))
        await ctx.send(f"Today's fortune: {fortune} 🙏 ")
        humanList.append(ctx.author.name)
    else:
        await ctx.send("You already got fortune today")

@client.command()
async def future(ctx):
    print("I see darkness inside you")
    await ctx.send("I see darkness inside you")
    time.sleep(3)
    print(client.user.name)
    print(ctx.author.name)
    print("Oh... My bad. It's your poop")
    await ctx.send("Oh... My bad. It's your poop")

@client.command()
async def justin(message):
    await message.send("Yo")
    time.sleep(2)
    await message.send("Is that you {}".format(message.author.name))

@client.command()
async def past(message):
    await message.send("The past is in the past")
    time.sleep(1)
    await message.send("Let it go, Let it go")
    time.sleep(1)
    await message.send("When I'll rise like the break of dawn")
    time.sleep(1)
    await message.send("Let it go, Let it go")
    time.sleep(1)
    await message.send("That perfect girl is gone")
    time.sleep(1)
    await message.send("Here I stand in the light of day")
    time.sleep(1)
    await message.send("Let the storm rage on")
    time.sleep(1)
    await message.send("The cold never bothered me anyway")

client.run(api_key)

while True:
    schedule.run_pending()
    time.sleep(1)
