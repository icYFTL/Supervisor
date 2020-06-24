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
                        [asyncio.run_coroutine_threadsafe(_p['member'].add_roles(x), loop) for x in _p['roles']]
                        asyncio.run_coroutine_threadsafe(_p['member'].remove_roles(
                            [x for x in bot.get_guild(_p['guild_id']).roles if
                             x.name == config.get('prisoner_role_name', '')][0]), loop)

            if update_time + timedelta(minutes=15) <= datetime.now():
                violators.clear()
                update_time = datetime.now()
            time.sleep(5)

    def start(self):
        hues.warn('JailEngine is being started')
        _th = Thread(target=self.routine)
        _th.start()
