import aiohttp
from discord.ext import commands
import discord
import os
import asyncio


def bot_task_callback(future: asyncio.Future) -> object:
    if future.exception():
        raise future.exception()
    return None


async def run_bot():
    bot = None
    session = None

    try:
        # Set up required intents
        intents = discord.Intents.default()
        intents.message_content = True  # if you need message content access

        # Initialize bot with intents
        bot = commands.Bot(command_prefix="%", intents=intents)

        # Create aiohttp session and attach to bot
        session = aiohttp.ClientSession()
        bot.session = session

        # Load all cogs from the cogs/ directory
        for file in os.listdir("cogs"):
            if file.endswith(".py") and not file.startswith("__"):
                await bot.load_extension(f"cogs.{file[:-3]}")

        # Start bot with token from environment variable
        await bot.start("OTAxNTU1NDkzNzkxNzQ0MDAx.GmBHJf.rv2dA4znzdCYGqrZeqjA5F0X88id1Xx7bN1Jms")

    finally:
        # Cleanup session and bot on shutdown
        if session and not session.closed:
            await session.close()
        if bot is not None:
            await bot.close()


# Run bot event loop (futureproofed for Python 3.13+)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    future = asyncio.ensure_future(run_bot(), loop=loop)
    future.add_done_callback(bot_task_callback)
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()
