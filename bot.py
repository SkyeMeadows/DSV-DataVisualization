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
filepath_weapon_names = os.path.join(BASE_DIR, "weapon_names.json")
filepath_attribute_names = os.path.join(BASE_DIR, "attribute_names.json")

with open(filepath_weapon_names) as file:
    weapon_names = json.load(file)

with open(filepath_attribute_names) as file:
    attribute_names = json.load(file)

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

bot = MyBot()


@bot.tree.command(name="compare_specific_weapons", description="Get a graph comparing a category of weapons.")
@app_commands.describe(
    weapon_one="Display Name of a weapon",
    weapon_two="Display Name of a weapon",
    trait_one="A trait or attribute you would like to compare",
    trait_two="A trait or attribute you would like to compare"
)
@app_commands.choices(
    weapon_one=[app_commands.Choice(name=w, value=w) for w in weapon_names],
    weapon_two=[app_commands.Choice(name=w, value=w) for w in weapon_names],
    trait_one=[app_commands.Choice(name=w,value=w) for w in attribute_names],
    trait_two=[app_commands.Choice(name=w,value=w) for w in attribute_names],
)
async def create_graph(
    interaction: discord.Interaction,
    weapon_one: str, 
    weapon_two: str,
    trait_one: str,
    trait_two: str,
    
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

    await interaction.followup.send(file=discord.File(graph_file_path))

bot.run(TOKEN)