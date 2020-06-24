from source.main.Main import *
from source.handlers.JailEngine import JailEngine

jailEngine = JailEngine()
jailEngine.start()

hues.warn('Bot is being started')
bot.run(config['token'])
