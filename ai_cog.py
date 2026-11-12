import asyncio
import requests
import discord
from discord.ext import commands

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = "llama3.1" 
        self.url = "http://localhost:11434/api/chat"

    def _call_model(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    @commands.command(name="ask")
    async def ask(self, ctx, *, prompt: str):
        async with ctx.typing():
            try:
                # Run blocking API call in a separate thread to prevent bot lag
                answer = await asyncio.to_thread(self._call_model, prompt)
                for start in range(0, len(answer), 2000):
                    await ctx.send(answer[start:start + 2000])
            except Exception as e:
                await ctx.reply(f"Error connecting to LLM: {e}")

async def setup(bot):
    await bot.add_cog(AICog(bot))
