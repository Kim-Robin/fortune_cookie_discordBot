import discord
from discord.ext import commands, tasks
from discord.flags import Intents
import random
import json
import time
import datetime
import os
import requests


userList: list = []
intents: Intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=["login ", "Login "], intents=intents)

api_key: str = os.environ.get("FORTUNE_COOKIE_DISCORD_KEY", "")
dirName: str = os.environ.get("FORTUNE_LOCATION", "")
tts_endpoint: str = os.environ.get("TTS_ENDPOINT", "")
voice_id: str = os.environ.get("VOICE_ID", "")

utc: datetime.timezone = datetime.timezone.utc
reset_time: datetime.time = datetime.time(hour=12, minute=13, tzinfo=utc)

fortune_json = open(dirName, "r")
data = json.loads(fortune_json.read())


def clear_human():
    print("reset happens")
    userList.clear()


@client.command()
async def fortune(ctx, *args):

    if "-v" in args:
        if ctx.author.name not in userList:
            index = random.randint(0, 356)
            fortune = data[index].get("fortune")
            await ctx.send(f"Today's fortune: {fortune} 🙏 ")
            userList.append(ctx.author.name)

            payload = {
                "text": fortune,
                "voice_id": voice_id, # todo: move voice id to service
                "stability": 0.15,
                "similarity_boost": 0.85,
                "style": 0.6,
                "use_speaker_boost": False,
             }

            response = requests.post(tts_endpoint, json=payload)

                # attach mp3 file to fortune
            if response.status_code == 200:
                    # save mp3 file
                mp3_filename = "fortune.mp3"
                with open(mp3_filename, "wb") as f:
                    f.write(response.content)

                await ctx.send(file=discord.File(mp3_filename))
            else:
                await ctx.send("TTS service failed. Could not generate audio.")
        else:
            await ctx.send("You already got fortune today")
    else:
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
