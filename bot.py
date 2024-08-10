import discord
from discord.ext import commands, tasks
import datetime
import pytz

botToken = ""
channelId = ""
maxSessionTimeMinutes = 60
aest_tz = pytz.timezone('Australia/Sydney')

class Session:
    def __init__(self):
        self.isActive = False
        self.sessionStartTime = 0
        self.sessionEndTime = 0
        self.breakTime = 0
        self.pausedTime = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print('Bot is ready!')
    break_reminder.start()
    check_session_time_limit.start()

@bot.command()
async def start(ctx):
    if session.isActive:
        await ctx.send("A session is already active!")
        return
    
    session.isActive = True
    session.sessionStartTime = datetime.datetime.now().timestamp()
    humanReadableTime = datetime.datetime.now(aest_tz).strftime("%H:%M:%S") 
    await ctx.send(f"New session started at {humanReadableTime}")

@bot.command()
async def end(ctx):
    if not session.isActive:
        await ctx.send("No session is active!")
        return
    
    await end_session(ctx.channel)

@bot.command()
async def pause(ctx):
    if not session.isActive:
        await ctx.send("No session is active!")
        return
    
    if session.pausedTime == 0:
        session.pausedTime = datetime.datetime.now().timestamp()
        await ctx.send("Session paused!")
    else:
        session.breakTime += datetime.datetime.now().timestamp() - session.pausedTime
        session.pausedTime = 0
        await ctx.send("Session unpaused!")

@tasks.loop(minutes=maxSessionTimeMinutes)
async def break_reminder():
    if session.isActive and session.pausedTime == 0:
        channel = bot.get_channel(channelId)
        await channel.send(f"**Take a break!** You've been studying for {maxSessionTimeMinutes} minutes.")

@tasks.loop(seconds=1)
async def check_session_time_limit():
    if session.isActive:
        current_time = datetime.datetime.now().timestamp()
        session_duration = current_time - session.sessionStartTime - session.breakTime
        if session_duration >= maxSessionTimeMinutes * 60:
            await end_session(bot.get_channel(channelId))

async def end_session(channel):
    session.isActive = False
    session.sessionEndTime = datetime.datetime.now().timestamp()
    duration = int(session.sessionEndTime - session.sessionStartTime - session.breakTime)
    human_readable_duration = str(datetime.timedelta(seconds=duration))

    await channel.send(f"Session ended. Total duration: {human_readable_duration}")
    break_reminder.stop()

bot.run(botToken)