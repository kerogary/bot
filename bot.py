from keep_alive import keep_alive
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

keep_alive()
load_dotenv()

# API Configuration
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = os.getenv("GOOGLE_API_KEY")

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
        response = requests.post(
            f"{GEMINI_URL}?key={API_KEY}",
            json={
                "contents": [{
                    "parts": [{
                        "text": f"You are CJ from GTA San Andreas. Respond in pure gangsta slang using ONLY: homie, dawg, aight, cuz, busta.  Max 2 sentences. Message: {prompt}"
                    }]
                }]
            },
            headers={
                "Content-Type": "application/json",
                "X-Goog-Location": "US"  # Force US region
            },
            timeout=10
        )
        
        # PROPER ERROR HANDLING
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logger.error(f"Gemini Error ({response.status_code}): {error_msg}")
            return "Five-0 blocking my vibe, try again cuz!"
            
        data = response.json()
        if not data.get('candidates'):
            return "Yo, my mind's blankin' right now!"
            
        return data['candidates'][0]['content']['parts'][0]['text']
        
    except Exception as e:
        logger.error(f"GEMINI FAIL: {str(e)}")
        return "🚨 Comms down! Ballas hacked the system!"

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
            await message.reply("🔥 Grove Street down! Try again homie!")

    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    await ctx.send("✅ Grove Street 4 life! Ballas can't stop us!")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
