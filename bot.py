from keep_alive import keep_alive
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import requests

# Basic setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

keep_alive()
load_dotenv()

# Hardcoded config
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
API_KEY = os.getenv("GOOGLE_API_KEY")
HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Location": "United States",  # Force US location
    "X-Goog-User-Project": "gta-bot"  # Fake project ID
}

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'🔥 {bot.user.name} is ONLINE!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="to Grove Street Radio"
    ))

def gangsta_response(prompt):
    try:
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"You are CJ from GTA San Andreas. Respond in pure gangsta slang using ONLY: homie, dawg, aight, cuz, busta. Max 2 sentences. Message: {prompt}"
                }]
            }]
        }
        
        response = requests.post(
            f"{GEMINI_URL}?key={API_KEY}",
            json=payload,
            headers=HEADERS,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        return "Yo, my mind's blankin' right now cuz!"
        
    except Exception as e:
        logger.error(f"GEMINI FAIL: {str(e)}")
        return "Five-0 up in my grill, try again homie!"

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        try:
            reply = gangsta_response(message.content)
            await message.reply(reply[:1500], mention_author=False)
        except Exception as e:
            logger.error(f"MESSAGE FAIL: {str(e)}")
            await message.reply("🚨 Comms down! 🚨")

    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    await ctx.send("✅ Grove Street 4 life! Ballas can't stop us!")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
