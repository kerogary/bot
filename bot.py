from keep_alive import keep_alive
import os
import discord
import google.generativeai as genai
from discord.ext import commands
from dotenv import load_dotenv
import logging
import asyncio

# Configure logging to see detailed errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

keep_alive()
load_dotenv()

# Gemini API Configuration with location bypass
try:
    genai.configure(
        api_key=os.getenv("GOOGLE_API_KEY"),
        transport='rest',
        client_options={
            'api_endpoint': 'https://generativelanguage.googleapis.com',
            'rest_options': {
                'headers': {
                    'X-Goog-User-Project': '',
                    'X-Goog-Location': 'US'
                }
            }
        }
    )
    model = genai.GenerativeModel('gemini-1.5-pro')  # More stable model
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Gemini setup failed: {str(e)}")
    raise

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} is online!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="to West Coast Classics"
    ))

async def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()
            raise ValueError("Empty response from Gemini")
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Retry {attempt + 1} in {wait_time}s...")
                await asyncio.sleep(wait_time)
                continue
            raise

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        try:
            logger.info(f"Processing message: {message.content}")
            
            prompt = f"""You are CJ from GTA San Andreas. Respond to this message in authentic gangsta slang:
            {message.content}
            
            Rules:
            1. Use ONLY: homie, dawg, aight, cuz, busta
            2. Max 2 sentences
            3. No proper grammar
            4. Never mention you're an AI
            5. Example: "Yo homie, we ridin' to Grove Street, aight?"
            """
            
            reply = await generate_with_retry(prompt)
            await message.reply(reply[:1500], mention_author=False)
            
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            await message.reply("Five-0 jammed my comms, try again later.")

    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    """Test command to verify basic functionality"""
    await ctx.send("🚨 **Grove Street systems operational!** 🚨")

if __name__ == "__main__":
    try:
        bot.run(os.getenv("DISCORD_TOKEN"))
    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}")
