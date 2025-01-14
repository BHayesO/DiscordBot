import json
from discord import Interaction
from emoji_config import TEAM_EMOJIS

TABLE_FILE = "table_data.json"
table = []
table_message_id = None
table_channel_id = None

def save_table_data():
    global table, table_message_id, table_channel_id
    with open(TABLE_FILE, "w") as file:
        json.dump({
            "table": table,
            "table_message_id": table_message_id,
            "table_channel_id": table_channel_id
        }, file)

def load_table_data():
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

def generate_table():
    if not table:
        return "La tabla está vacía. Usa `/new_member` para agregar filas."

    col1_width = max(len(row["Nickname PoGo"]) for row in table) if table else len("Nickname PoGo")
    col2_width = max(len(row["Team"]) for row in table) if table else len("Team")
    col3_width = max(len(row["Codigo"]) for row in table) if table else len("Codigo")

    col1_width = max(col1_width, len("Nickname PoGo"))
    col2_width = max(col2_width, len("Team"))
    col3_width = max(col3_width, len("Codigo"))

    table_message = f"| {'Nickname PoGo':<{col1_width}} | {'Team':<{col2_width}} | {'Codigo':<{col3_width}} |\n"
    table_message += f"|{'-' * (col1_width + 2)}|{'-' * (col2_width + 2)}|{'-' * (col3_width + 2)}|\n"

    for row in table:
        team_with_emoji = f"{TEAM_EMOJIS.get(row['Team'], '')} {row['Team']}"
        table_message += f"| {row['Nickname PoGo']:<{col1_width}} | {team_with_emoji:<{col2_width}} | {row['Codigo']:<{col3_width}} |\n"

    return table_message

async def add_member_to_table(interaction: Interaction, nickname: str, team: str, codigo: str):
    global table, table_message_id, table_channel_id

    if not codigo.isdigit() or len(codigo) != 12:
        await interaction.response.send_message(
            "❌ El código debe contener exactamente **12 números**. Intenta de nuevo.",
            ephemeral=True
        )
        return False

    table.append({"Nickname PoGo": nickname, "Team": team, "Codigo": codigo})
    table = sorted(table, key=lambda x: x["Nickname PoGo"])

    if not table_message_id or not table_channel_id:
        await interaction.response.send_message(
            "❌ No se encontró un mensaje de tabla. Usa `!create_table` primero.",
            ephemeral=True
        )
        return False

    channel = interaction.client.get_channel(table_channel_id)
    if not channel:
        await interaction.response.send_message(
            "❌ No se pudo encontrar el canal.",
            ephemeral=True
        )
        return False

    message = await channel.fetch_message(table_message_id)
    updated_table = generate_table()
    await message.edit(content=updated_table)
    save_table_data()
    await interaction.response.send_message(
        f"✔️ Fila agregada: **{nickname}** - **{team}** - **{codigo}**",
        ephemeral=True
    )
    return True
