import asyncio
import os

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=";", intents=intents)

MODEL = "llama3.1"
URL = "http://localhost:11434/api/chat"


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


if not token:
    raise RuntimeError("TOKEN is missing. Set it in your .env file.")

bot.run(token)
