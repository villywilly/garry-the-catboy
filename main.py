import asyncio
import os
import random
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
prf = ";"
bot = commands.Bot(command_prefix=prf, intents=intents)

MODEL = "llama3.1"
URL = "http://localhost:11434/api/chat"
@bot.event
async def on_ready():
    print(f"Online as {bot.user}")
async def on_command_error(ctx, error):
    print(f"Command error: {error!r}")
def call_model(prompt: str) -> str:
    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["message"]["content"].strip()

@bot.command(name="prefix")
async def prefix(ctx, prfix: str):
    prf = prfix
    ctx.send(f"Set {prf} as the prefix.")
@bot.command(name="ask")
async def ask(ctx, *, prompt: str):
    async with ctx.typing():
        try:
            answer = await asyncio.to_thread(call_model, prompt)

            # Discord messages have a 2,000-character limit.
            for start in range(0, len(answer), 2000):
                await ctx.send(answer[start:start + 2000])

        except requests.RequestException as e:
            await ctx.reply(f"Error connecting to the model: {e}")
        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")

@bot.command(name="ping")
async def ping(ctx):
   await ctx.send("Pong 🇻🇺🏳️‍🌈🇨🇳🇦🇷")
@bot.command(name="say")
async def say(ctx, *, said: str):
    await ctx.send(said)
@bot.command(name="pick")
async def pick(ctx, *, said: str):
    poss = [True, False]
    await ctx.send(f"{said} is {random.choice(poss)}!")
@bot.command(name="gayrate")
async def gayrate(ctx, person: str):
    await ctx.send(f"{person} is {random.randint(1,100)}% gay!")
@bot.command(name="ship")
async def ship(ctx, p1: str, p2: str):
    comp = random.randint(0,100)
    spmsg = None
    if comp <= 25:
        spmsg = "Unlikely"
    elif comp <= 50:
        spmsg = "Its possible 🇦🇹🇩🇪🇭🇺⚛️🇵🇸🇦🇷🏳️‍🌈🏳️‍⚧️🇻🇺🇺🇸🇨🇭🇧🇦🇨🇳"
    elif comp <= 75:
        spmsg = "Pretty likely to happen "
    elif comp <= 100:
        spmsg = "Guaranteed!!"
    await ctx.send(f"Shipping {p1} and {p2}\nThe compatibility is {comp}%\n{spmsg}")
@bot.command(name="guide")
async def guide(ctx, optional=None):
    match optional:
        case "list":
            await ctx.send("""All commands:
                           ;gayrate (person) - Prints out a random percent value for how gay this person is
                           ;ping - The bot sends a message saying "pong" if it is online and has required permissions
                           ;say (query) - The bot will say what you typed in the query parameter
                           ;ship (person1) (person2) - Ships the two selected people
                           ;guide [whatYouNeedHelpWith] - Prints out a help menu, or various sub menus.
                           ;ask (prompt) - Send a prompt to a local LLM (On this server we use Llama 3.1 on this instance of Garry TC)
                           Note: (required) [optional]
                           Note: With the exception of ;ask, and ;say: Please type other parameters in CamelCase or snake_case as spaces will seperate into different parameters.""")
        case _:
            await ctx.send("""Garry The Catboy (or Garry TG for short) is a discord bot mainly used for random fun in our discord server.
            Developed by <@1315852798742757471> :pink_heart: :purple_heart: :blue_heart: with some help by <@1274180379036614750> :rainbow_flag:.\nIf you want to self host this bot, or contribute to it, it is available at [notacircle.net/ql.php?u=2](https://notacircle.net/ql.php?u=2) under the Gnu General Public License V3 (open source!!)More open source notes: This instance of Garry TG is hosted on a Fedora Linux server if you care about that. (which you prolly dont).
            Help:
            - guide list = list all commands\nAll commands use the semicolon (;) for the command prefix.""")
if not token:
    raise RuntimeError("TOKEN is missing. Set it in your .env file.")

bot.run(token)

