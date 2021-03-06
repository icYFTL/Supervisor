from Core import punished, bot, config, loop, violators
from datetime import datetime, timedelta
import time
import hues
from threading import Thread
import asyncio


class JailEngine(object):
    def routine(self):
        update_time = datetime.now()
        while True:
            if punished:
                for _p in punished:
                    if _p['date_to'] <= datetime.now():
                        asyncio.run_coroutine_threadsafe(JailEngine.unpunish(_p), loop)
                        punished.remove(_p)
            if update_time + timedelta(minutes=15) <= datetime.now():
                violators.clear()
                update_time = datetime.now()
            time.sleep(5)

    @staticmethod
    async def unpunish(user):
        if user['roles'] and (len(user['roles']) and user['roles'][0].name != config.get('prisoner_role_name')):
            await user['member'].add_roles(*user['roles'][1:])
        await user['member'].remove_roles(
            [x for x in bot.get_guild(user['guild_id']).roles if
             x.name == config.get('prisoner_role_name', '')][0])

    def start(self):
        hues.warn('JailEngine is being started')
        _th = Thread(target=self.routine)
        _th.start()
