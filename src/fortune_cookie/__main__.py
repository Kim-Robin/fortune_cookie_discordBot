import discord
from discord.ext import commands, tasks
from discord.flags import Intents
import random
import json
import time
import datetime
import os

userList: list = []
intents: Intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=["login ", "Login "], intents=intents)

api_key: str = os.environ.get("FORTUNE_COOKIE_DISCORD_KEY", "")
dirName: str = os.environ.get("FORTUNE_LOCATION", "")

utc: datetime.timezone = datetime.timezone.utc
reset_time: datetime.time = datetime.time(hour=12, minute=13, tzinfo=utc)

fortune_json = open(dirName, "r")
data = json.loads(fortune_json.read())


def clear_human():
    print("reset happens")
    userList.clear()


@client.command()
async def fortune(ctx):
    if ctx.author.name not in userList:
        index = random.randint(0, 356)
        fortune = data[index].get("fortune")
        await ctx.send(f"Today's fortune: {fortune} 🙏 ")
        userList.append(ctx.author.name)
    else:
        await ctx.send("You already got fortune today")


@client.command()
async def future(ctx):
    await ctx.send("I see darkness inside you")
    time.sleep(3)
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


@tasks.loop(time=reset_time)
async def schedule_daily():
    channel_id: str = os.environ.get("FORTUNE_CLIENT_CHANNEL", "")
    channel = client.get_channel(int(channel_id))

    if channel:
        if isinstance(channel, discord.channel.TextChannel):
            clear_human()
            await channel.send("Fortune cookie Re-Calibrated. Have a good day!")


@client.event
async def on_ready():
    print("Bot is ready.")
    await schedule_daily.start()


def main():
    client.run(api_key)
    print("closing")
