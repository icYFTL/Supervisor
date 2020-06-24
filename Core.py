from discord.ext import commands
import json
import hues

punished = list()
violators = list()

config = json.loads(open('Config.json', 'r').read() or {})

if not config:
    hues.error("No Config.json passed or it's empty.")
    exit()

if not config.get('token'):
    hues.error("No bot token passed.")
    exit()

bot = commands.Bot(command_prefix='#')
loop = bot.loop
