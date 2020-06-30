from Core import *
from discord import message, utils, Member
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
            await ctx.send(
                f'Who aRe yOu, {ctx.author.mention}? Anyway, one more time you\'ll try to punish somebody - I\'ll punish y0u!')
            violators.append(ctx.author)
        else:
            await ctx.send('I will play with y0ur a$$, ' + ctx.author.mention)
            ctx.message.mentions.clear()  # TODO: REFACTOR
            ctx.message.mentions.append(ctx.author)
            ctx.message.author = None
            await jail(ctx, 1)
        return False

    # Check punished members's roles
    for _permitted in config.get('permitted_roles', {}):
        for _member in members:
            for _role in _member.roles:
                if _role.name == _permitted:
                    permit = _member

    if isinstance(permit, Member):
        await ctx.send(f'{permit.mention} is too big for you, {ctx.author.mention}')
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
    _members = [utils.get(ctx.message.guild.members, id=x.id) for x in
                ctx.message.mentions]  # Get members from mentions
    for _member in _members:
        punished.append(
            {'member': _member, 'date_to': datetime.now() + timedelta(minutes=delay), 'roles': copy(_member.roles),
             'guild_id': ctx.message.guild.id})  # Save roles and set imprisonment time
        await _member.remove_roles(*_member.roles[1:])  # Remove all roles
        await _member.add_roles(  # Add prisoner's role
            [x for x in bot.get_guild(ctx.message.guild.id).roles if
             x.name == config.get('prisoner_role_name', '')][0])

        stat.add_user(_member.id)  # Add user to statistic database
        stat.increment_imprisonment_counter(_member.id)  # Increment imprisonment counter
        stat.update_time(_member.id, delay)  # Update total jailed time
        if ctx.message.author:  # If other user jailed prisoner
            stat.add_dominus(_member.id, ctx.message.author.id)
        else:  # If bot jailed prisoner
            stat.add_dominus(_member.id, bot.user.id)

        try:  # If user not in voice channel at the moment
            await _member.move_to(utils.get(ctx.message.guild.channels, name=config['prison_channel_name']))
        except:
            pass

    await ctx.send(
        f'Welcome to the club, {", ".join([x.mention for x in ctx.message.mentions])} for {delay} minute{"s" if delay > 1 else ""}')


@bot.command('top')
async def on_top(ctx: message):
    from collections import Counter
    msg_template = '#{iter}. <@{username}>\nImprisonment count: {icounter}\nTotal time in jail: {total_time} minutes\nLoved by: {dominuses}\n\n'
    users: list = stat.get_sorted_users()
    if users:
        for x in users:
            x.kicked_by = Counter(x.kicked_by)
        await ctx.send("Here's my favorite boys:\n" + '\n'.join(
            [msg_template.format(iter=x + 1,
                                 username=users[x].id,
                                 icounter=users[x].imprisonment_counter,
                                 total_time=users[x].total_time,
                                 dominuses=' '.join(
                                     [f'<@{str(i)}> x{users[x].kicked_by[i]}' for i in users[x].kicked_by]))
             for x in range(len(users))]))
    else:
        await ctx.send('I don\'t remember no one sweety aS$.')


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
        await ctx.send('I can\'t find this tasty as$ :(')
    else:
        await ctx.send(
            'I remembered your sweety asses. See you again, ' + ','.join([x.mention for x in ctx.message.mentions]))