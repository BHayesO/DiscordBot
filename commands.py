from discord import app_commands
from discord.ext import commands
from table_manager import save_table_data, generate_table, add_member_to_table
from whatsapp_utils import send_whatsapp_message

def register_commands(bot: commands.Bot):
    @bot.command(name="create_table")
    async def create_table(ctx):
        from table_manager import table_message_id, table_channel_id

        message = await ctx.send(generate_table())
        table_message_id = message.id
        table_channel_id = ctx.channel.id
        save_table_data()

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
    async def new_member(interaction, nickname: str, team: app_commands.Choice[str], codigo: str):
        result = await add_member_to_table(interaction, nickname, team.value, codigo)
        if not result:
            return

    @bot.command(name="send_whatsapp")
    async def send_whatsapp(ctx, *, message: str):
        """
        Command to send a WhatsApp message to the Twilio Sandbox.
        """
        success = send_whatsapp_message(message)
        if success:
            await ctx.send(f"✔️ WhatsApp message sent: `{message}`")
        else:
            await ctx.send("❌ Failed to send WhatsApp message. Check the logs.")