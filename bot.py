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
