from discord.ext import commands, tasks
import discord
import datetime
import pytz

botToken = ""
channelId = 1265944846238220329
maxSessionTimeMinutes = 30
aest_tz = pytz.timezone('Australia/Sydney')

class Session:
    isActive: bool = False
    sessionStartTime: float = 0
    sessionEndTime: float = 0
    breakTime: float = 0
    pausedTime: float = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.command()
async def start(ctx):
    if session.isActive:
        await ctx.send("A session is already active!")
        return
    
    session.isActive = True
    session.sessionStartTime = ctx.message.created_at.timestamp()
    humanReadableTime = datetime.datetime.now(aest_tz).strftime("%H:%M:%S") 
    break_reminder.start()
    await ctx.send(f"New session started at {humanReadableTime}")

@bot.command()
async def end(ctx):
    if not session.isActive:
        await ctx.send("No session is active!")
        return
    
    session.isActive = False
    session.sessionEndTime = ctx.message.created_at.timestamp()
    duration = session.sessionEndTime - session.sessionStartTime - session.breakTime - session.pausedTime
    humanReadableDuration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {humanReadableDuration}")

@bot.command()
async def pause(ctx):
    if not session.isActive:
        await ctx.send("No session is active!")
        return
    
    if session.pausedTime == 0:
        session.pausedTime = ctx.message.created_at.timestamp()
        await ctx.send("Session paused!")
    else:
        session.pausedTime = ctx.message.created_at.timestamp() - session.pausedTime
        await ctx.send("Session unpaused!")

@tasks.loop(minutes=maxSessionTimeMinutes, count=2)
async def break_reminder():
