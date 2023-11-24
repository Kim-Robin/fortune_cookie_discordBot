import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
import json
import time
import datetime
import os
import requests, json, random, datetime, asyncio

humanList = []
intents = discord.Intents.default()

client = commands.Bot(command_prefix=['login ', 'Login '], intents=intents)

# dirName = os.path.dirname(__file__) + '/fortune.json'
dirName = os.environ.get("FORTUNE_LOCATION")
print(dirName)

f = open(dirName, "r")
data = json.loads(f.read())
print(type(data))
print(len(data))


def clear_human():
    print("reset happens")
    humanList.clear()
    print(humanList)

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

@tasks.loop(hours=24)
async def schedule_daily():
    # channel = client.get_channel(708819813396643940)
    channel_id = os.environ.get("FORTUNE_CLIENT_CHANNEL")
    channel = client.get_channel(int(channel_id))

    clear_human()
    await channel.send("Fortune cookie Re-Calibrated. Have a good day!")

@client.event
async def on_ready():
    print('Bot is ready.')
    await schedule_daily()

scheduler = AsyncIOScheduler()
scheduler.add_job(schedule_daily.start, trigger="cron", hour=7, minute=48, second=21)

api_key = os.environ.get("FORTUNE_COOKIE_DISCORD_KEY")
client.run(api_key)

