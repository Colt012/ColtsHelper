# twitchint.py
import requests
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve credentials from .env
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))  # Convert to int
STREAMERS = ["colt_m249", "bobbyk211", "II_Reithin_II", "sylphrena_daniik"]  # Replace with actual Twitch usernames

# Function to check if a streamer is live
async def is_stream_live(user):
    url = f"https://api.twitch.tv/helix/streams?user_login={user}"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}"
    }

    print(f"Checking stream status for {user}...")  # Debug log

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            print(f"✅ {user} is LIVE!")  # Debug log
            return True
        else:
            print(f"❌ {user} is OFFLINE.")  # Debug log
            return False

    except Exception as e:
        print(f"🚨 Error checking stream for {user}: {e}")
        return False

# Background task to check Twitch stream status
async def check_stream_status(client):
    await client.wait_until_ready()
    channel = client.get_channel(DISCORD_CHANNEL_ID)

    if not channel:
        print("⚠️ Error: Could not find the Discord channel. Make sure the ID is correct.")
        return

    live_streamers = set()  # Keep track of who is already live

    while not client.is_closed():
        print("🔄 Checking stream statuses...")  # Debug log

        for streamer in STREAMERS:
            try:
                live = await is_stream_live(streamer)

                if live and streamer not in live_streamers:
                    message = f"🎥 **{streamer}** is now LIVE on Twitch! Watch here: https://www.twitch.tv/{streamer}"
                    await channel.send(message)
                    live_streamers.add(streamer)
                    print(f"📢 Announced live stream: {streamer}")  # Debug log

                elif not live and streamer in live_streamers:
                    live_streamers.remove(streamer)
                    print(f"⚠️ {streamer} went offline.")  # Debug log

            except Exception as e:
                print(f"🚨 Error checking {streamer}: {e}")

        print("⏳ Waiting 600 seconds before next check...")  # Debug log
        await asyncio.sleep(600)
