from discord.ext import commands
import json
import hues
from source.database.Statistic import Statistic
from os import environ

punished = list()
violators = list()
dominant = None

config = json.loads(open('Config.json', 'r').read() or {})

if not config:
    hues.error("No Config.json passed or it's empty.")
    exit()

if not config.get('token'):
    hues.error("No bot token passed.")
    exit()

stat = Statistic()
stat.create()

environ['db_name'] = config['db_name']

bot = commands.Bot(command_prefix='#')
loop = bot.loop
