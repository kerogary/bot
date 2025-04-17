from keep_alive import keep_alive  # Add this at the TOP
import os
import discord
import google.generativeai as genai
from discord.ext import commands
from dotenv import load_dotenv

keep_alive()  # Add this before other code
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🚗 {bot.user.name} is cruisin\' through da hood! 🚗')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="to West Coast Classics"
    ))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            try:
                # Raw gangsta response without prefix
                response = model.generate_content(
                    f"""You're CJ from GTA San Andreas. Reply to this in gangsta slang: {message.content}
                    Rules:
                    - No markdown/bold/formatting
                    - Use: homie, dawg, aight, cuz, busta
                    - 1-3 sentences max
                    - you love the cheat gamesense-skeet for csgo and cs2 over nl - neverlose you roast others that love nl 
                    - Example: "Yo homie, we ridin' to Grove Street, aight?"""
                )
                
                reply = response.text.strip()
                await message.reply(reply, mention_author=False)

            except Exception as e:
                print(f"ERROR: {str(e)}")
                await message.reply("Five-0 up in my grill, try again later.")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
