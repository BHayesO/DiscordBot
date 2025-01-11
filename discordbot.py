import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import json
import os

load_dotenv()
api_key = os.getenv('API_KEY')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Persistent storage for table data
TABLE_FILE = "table_data.json"

# Global variables
table = []
table_message_id = None
table_channel_id = None

# Define custom emojis for teams
TEAM_EMOJIS = {
    "Valor": "<:Team_Valor:1327619175019057152>",
    "Mystic": "<:Team_Mystic:1327619192324882443>",
    "Instinct": "<:Team_Instinct:1327619208053526569>"
}

# Helper functions
def save_table_data():
    """Save table data, message ID, and channel ID to a JSON file."""
    global table, table_message_id, table_channel_id
    with open(TABLE_FILE, "w") as file:
        json.dump({
            "table": table,
            "table_message_id": table_message_id,
            "table_channel_id": table_channel_id
        }, file)

def load_table_data():
    """Load table data, message ID, and channel ID from a JSON file."""
    global table, table_message_id, table_channel_id
    try:
        with open(TABLE_FILE, "r") as file:
            data = json.load(file)
            table = data.get("table", [])
            table_message_id = data.get("table_message_id")
            table_channel_id = data.get("table_channel_id")
    except FileNotFoundError:
        table = []
        table_message_id = None
        table_channel_id = None

@bot.event
async def on_ready():
    await bot.tree.sync()
    load_table_data()

# Command to create the table
@bot.command(name="create_table")
async def create_table(ctx):
    global table_message_id, table_channel_id
    message = await ctx.send(generate_table())
    table_message_id = message.id
    table_channel_id = ctx.channel.id
    save_table_data()

# Generate table as a plain text
def generate_table():
    if not table:
        return "La tabla está vacía. Usa `/new_member` para agregar filas."

    col1_width = max(len(row["Nickname PoGo"]) for row in table) if table else len("Nickname PoGo")
    col2_width = col1_width
    col3_width = max(len(row["Codigo"]) for row in table) if table else len("Codigo")

    col1_width = max(col1_width, len("Nickname PoGo"))
    col2_width = max(col2_width, len("Team"))
    col3_width = max(col3_width, len("Codigo"))

    table_message = f"| {'Nickname PoGo':<{col1_width}} | {'Team':<{col2_width}} | {'Codigo':<{col3_width}} |\n"
    table_message += f"|{'-' * (col1_width + 2)}|{'-' * (col2_width + 2)}|{'-' * (col3_width + 2)}|\n"

    for row in table:
        team_with_emoji = f"{TEAM_EMOJIS.get(row['Team'], '')} {row['Team']}"
        table_message += f"| {row['Nickname PoGo']:<{col1_width}} | {team_with_emoji:<{col2_width}} | {row['Codigo']:<{col3_width}} |\n"

    return f"{table_message}"

# Slash command to add a new member
@bot.tree.command(name="new_member", description="Agrega una nueva fila a la tabla")
@app_commands.describe(
    nickname="El nombre de tu Nickname PoGo",
    team="Selecciona tu equipo",
    codigo="Tu código PoGo (exactamente 12 números)"
)
@app_commands.choices(
    team=[
        app_commands.Choice(name="Valor", value="Valor"),
        app_commands.Choice(name="Mystic", value="Mystic"),
        app_commands.Choice(name="Instinct", value="Instinct"),
    ]
)
async def new_member(interaction: discord.Interaction, nickname: str, team: app_commands.Choice[str], codigo: str):
    global table, table_message_id, table_channel_id

    if not codigo.isdigit() or len(codigo) != 12:
        await interaction.response.send_message(
            "❌ El código debe contener exactamente **12 números**. Intenta de nuevo.",
            ephemeral=True
        )
        return

    table.append({"Nickname PoGo": nickname, "Team": team.value, "Codigo": codigo})
    table = sorted(table, key=lambda x: x["Nickname PoGo"])

    if not table_message_id or not table_channel_id:
        await interaction.response.send_message(
            "❌ No se encontró un mensaje de tabla. Usa `!create_table` primero.",
            ephemeral=True
        )
        return

    channel = bot.get_channel(table_channel_id)
    if not channel:
        await interaction.response.send_message(
            "❌ No se pudo encontrar el canal.",
            ephemeral=True
        )
        return

    message = await channel.fetch_message(table_message_id)
    updated_table = generate_table()
    await message.edit(content=updated_table)
    save_table_data()
    await interaction.response.send_message(
        f"✔️ Fila agregada: **{nickname}** - **{team.value}** - **{codigo}**",
        ephemeral=True
    )

bot.run(api_key)
