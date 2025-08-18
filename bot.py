import discord # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from discord import Interaction, app_commands # type: ignore
from discord.ext import commands # type: ignore
from typing import Literal, Optional  # For fixed choices
import datetime
import json
import asyncio
import logging
import sys
import subprocess
import dotenv
# ===== START BASIC BOT =====

# Bot Invite Link = https://discord.com/oauth2/authorize?client_id=1405904972142477475&permissions=274878024704&integration_type=0&scope=bot

# Log levels:
# - DEBUG
# - INFO
# - WARNING
# - ERROR
# - CRITICAL

# Absolute path to the directory containing THIS script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

venv_python = sys.executable

# Setting up Logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "BotLog.txt"),
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S' 
)

log = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Slash commands synced!")

@bot.tree.command(name="shutdown", description="Shuts down the bot (admin only)")
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id == 305861137440833536:
        await interaction.response.send_message("Shutting down...", ephemeral=True)
        await bot.change_presence(status=discord.Status.offline)
        await bot.close()
    else:
        await interaction.response.send_message("You do not have permission!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")
# ===== END BASIC BOT =====

# Paths
graphing_script_path = os.path.join(BASE_DIR, "graph.py")
graph_file_path = os.path.join(BASE_DIR, "Graphs", "graph_memory.png")


@bot.tree.command(name="compare_specific_weapons", description="Get a graph comparing a category of weapons.")
@app_commands.describe(
    weapon_one="Display Name of a weapon",
    weapon_two="Display Name of a weapon",
    trait_one="A trait/attribute you would like to compare",
    trait_two="A trait/attribute you would like to compare"
)
async def create_graph(
    interaction: discord.Interaction,
    weapon_one: Literal["M240 Cyclone Strike Cannon", "M480 Hurricane Strike Cannon", "M600 Typhoon Strike Cannon"], 
    weapon_two: Literal["M240 Cyclone Strike Cannon", "M480 Hurricane Strike Cannon", "M600 Typhoon Strike Cannon"],
    trait_one: Literal["Points", "Range (Km)", "Projectile Speed (m/s)", "Firerate (rounds/s)", "Shots in Clip", "Penetration/Clip (HA Blocks)", "Splash Radius (meters)", "Cycle Time (seconds)", "Max Energy Draw/s (MW)", "Charge Reload Time (seconds)", "Effective Integrity"],
    trait_two: Optional[Literal["Points", "Range (Km)", "Projectile Speed (m/s)", "Firerate (rounds/s)", "Shots in Clip", "Penetration/Clip (HA Blocks)", "Splash Radius (meters)", "Cycle Time (seconds)", "Max Energy Draw/s (MW)", "Charge Reload Time (seconds)", "Effective Integrity"]]
):

    async def process():
        command = [
            venv_python,
            str(graphing_script_path),
            "--weapon_one", str(weapon_one),
            "--weapon_two", str(weapon_two),
            "--trait_one", str(trait_one),
            
        ]
        if trait_two:
            command.extend(["--trait_two", str(trait_two)])

        log.debug(f"Running subprocess command: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Graph Script failed with code {result.returncode}")


    try:
        await asyncio.wait_for(process(), timeout=30)
    except asyncio.TimeoutError:
        await interaction.followup.send("Process took too long (30s timeout).", ephemeral=True)

    await interaction.response.send_message(file=discord.File(graph_file_path))

bot.run(TOKEN)