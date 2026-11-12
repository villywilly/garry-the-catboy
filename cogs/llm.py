import asyncio
import requests
from discord.ext import commands

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"  # Change to your Ollama model name


def ask_model(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["message"]["content"].strip()


class Llm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask")
    async def ask(self, ctx, *, prompt: str):
        async with ctx.typing():
            try:
                answer = await asyncio.to_thread(ask_model, prompt)
            except requests.RequestException:
                await ctx.reply("I couldn't reach the model. Check that it’s running and the model name is correct.")
                return

        for start in range(0, len(answer), 2000):
            await ctx.reply(answer[start:start + 2000])


async def setup(bot):
    await bot.add_cog(Llm(bot))
