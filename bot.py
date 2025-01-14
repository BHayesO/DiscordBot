import discord
from discord.ext import commands
from dotenv import load_dotenv
from commands import register_commands
from table_manager import load_table_data

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Set up bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    load_table_data()
    print(f"Bot connected as {bot.user}")

# Register commands
register_commands(bot)

# Run bot
bot.run(api_key)
