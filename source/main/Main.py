from Core import *
from discord import message, utils
from copy import copy
from datetime import datetime, timedelta
from source.handlers.JailEngine import JailEngine


async def checks(ctx: message, members: list) -> bool:
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
        return False

    # Check punished members's roles
    for _permitted in config.get('permitted_roles', {}):
        for _member in members:
            for _role in _member.roles:
                if _role.name == _permitted:
                    permit = False
    if not permit:
        await ctx.send('He is too big for you')
        return False

    if len(ctx.message.content.split()) < 2 or not ctx.message.mentions:
        await ctx.send('What the fuck is this?')
        return False

    return True


@bot.command('punish')
async def on_punish(ctx: message) -> None:
    members = ctx.message.mentions

    if not await checks(ctx, members):
        return

    delay: int = 1

    try:
        delay = int(ctx.message.content.split()[2])
    except:
        pass

    if delay > 60:
        await ctx.send('So LoNg period.')
        return

    if delay < 1:
        await ctx.send('You\'re bad b0y!')
        return

    await jail(ctx, delay)


async def jail(ctx: message, delay: int) -> None:
    _members = [utils.get(ctx.message.guild.members, id=x.id) for x in ctx.message.mentions]
    for _member in _members:
        punished.append(
            {'member': _member, 'date_to': datetime.now() + timedelta(minutes=delay), 'roles': copy(_member.roles),
             'guild_id': ctx.message.guild.id})
        await _member.remove_roles(*_member.roles[1:])
        await _member.add_roles(
            [x for x in bot.get_guild(ctx.message.guild.id).roles if
             x.name == config.get('prisoner_role_name', '')][0])

        try:
            await _member.move_to(utils.get(ctx.message.guild.channels, name=config['prison_channel_name']))
        except:
            pass

    await ctx.send(f'Welcome to the club, {", ".join([x.mention for x in ctx.message.mentions])} for {delay} minutes')


@bot.command('unpunish')
async def on_unpunish(ctx: message):
    if not await checks(ctx, ctx.message.mentions):
        return

    unpunished: bool = False

    for user in ctx.message.mentions:
        for _p in punished:
            if _p['member'] == user:
                await JailEngine.unpunish(_p)
                punished.remove(_p)
                unpunished = True

    if not unpunished:
        await ctx.send('I can\'t find this tasty ass :(')
    else:
        await ctx.send(
            'I remembered your sweety asses. See you again, ' + ','.join([x.mention for x in ctx.message.mentions]))

# @bot.command('dominant')
# async def on_dominant(ctx: message) -> None:
#     from random import shuffle, randint
#     global dominant
#
#     if not dominant:
#         _members = copy(ctx.guild.members)
#         shuffle(_members)
#         dominant = _members[randint(0, len(_members) - 1)]
#     else:
#         await ctx.send(f'Until 00:00 gachi bos is {dominant.name}')
#         return
#
#     await ctx.send(f'New gachi bos is {dominant.name}')
