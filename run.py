import asyncio
import discord
from discord.ext import commands
import os
import main, ai
from dotenv import load_dotenv

# 2. Call this function BEFORE 
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=";", intents=intents)

#async def load_extensions():
    # This loads ai_cog.py
#    await bot.load_extension("ai_cog")
    #await bot.load_extension("main")

#async def main():
#    async with bot:
#        await load_extensions()
#        await bot.start(os.environ["TOKEN"])

asyncio.run(main())
