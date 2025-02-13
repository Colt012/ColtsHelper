import discord
import asyncio
import os
from dotenv import load_dotenv
import twitchint  # Import the Twitch integration module

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize Discord Bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Event when bot is ready
@client.event
async def on_ready():
    print(f"🤖 Logged in as {client.user}!")
    print("🚀 Starting stream status checker...")
    client.loop.create_task(twitchint.check_stream_status(client))  # Pass the bot client

# Run the bot
client.run(DISCORD_TOKEN)