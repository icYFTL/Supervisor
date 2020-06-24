from Core import config, bot, hues, punished, violators
from discord import message, utils
from copy import copy
from datetime import datetime, timedelta


@bot.command('punish')
async def on_punish(ctx: message):
    permit: bool = False
    # Check sender's permissions
    for _permitted in config.get('permitted_roles', {}):
        for _role in ctx.author.roles:
            if _permitted == _role.name and not permit:
                permit = True
                break

    if not permit:
        if ctx.author not in violators:
            await ctx.send('Who aRe yOu? Anyway, one more time you\'ll try to punish somebody - I\'ll punish y0u!')
            violators.append(ctx.author)
        else:
            await ctx.send('I will play with y0ur a$$!')
            await jail([ctx.author], ctx, 1)
        return

    # Check punished members's roles
    members = [utils.get(ctx.message.guild.members, id=x.id) for x in ctx.message.mentions]
    for _permitted in config.get('permitted_roles', {}):
        for _member in members:
            for _role in _member.roles:
                if _role.name == _permitted:
                    permit = False
    if not permit:
        await ctx.send('He is too big for you')
        return

    delay: int = 1

    try:
        delay = int(ctx.message.content.split()[2])
    except:
        pass

    if delay > 60:
        await ctx.send('So LoNg period.')
        return

    await jail(members, ctx, delay)


async def jail(members: list, ctx: message, delay: int) -> None:
    for _member in members:
        punished.append(
            {'member': _member, 'date_to': datetime.now() + timedelta(minutes=delay), 'roles': copy(_member.roles),
             'guild_id': ctx.message.guild.id})

        for _role in _member.roles:
            if _role.name != '@everyone':
                await _member.remove_roles(_role)

        await _member.add_roles(
            [x for x in bot.get_guild(ctx.message.guild.id).roles if
             x.name == config.get('prisoner_role_name', '')][0])

        await _member.move_to(utils.get(ctx.message.guild.channels, name='ТЮРЬМА'))

    await ctx.send(f'Welcome to the club: {", ".join([x.name for x in members])} for {delay} minutes')
