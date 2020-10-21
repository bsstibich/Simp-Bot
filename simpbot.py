import discord
from discord.ext import commands
import os
import json
import random
client = commands.Bot(command_prefix = ';')
channel = 0#general channel ID here
token = ''#bot token here

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#adds 1 or more simp points to whoever is tagged and sends a message saying how many points they have afterwards
#command is (;simp @user 1 infraction text)
#1 may be replaced with whatever number and everything after will be used as the infraction text
@client.command()
#@commands.has_role('CAD Officer')
async def simp(ctx, mention, value=1, *, infraction):
    with open('points.json', 'r') as f:
        users = json.load(f)
    for user in ctx.message.mentions:
        tagid = str(ctx.message.mentions[0].id)
        await update_data(users, tagid)
        start_level = users[tagid]['simp level']
        await add_point(users, tagid, value)
        await points_message(users, tagid, ctx.message, value, infraction, channel, start_level)
    with open('points.json', 'w') as f:
        json.dump(users, f)

#checks the simp points of caller of the message
#command is (;checksimp)
@client.command()
#@commands.has_role('CAD Officer')
async def checksimp(ctx):
    with open('points.json', 'r') as f:
        users = json.load(f)
    username = ctx.message.mentions[0].mention
    tagid = str(ctx.message.mentions[0].id)
    await update_data(users, tagid)
    await ctx.message.channel.send(f"{username} has {users[tagid]['points']} simp points")

    with open('points.json', 'w') as f:
        json.dump(users, f)
#removes a simp point from the tagged user
#command is (;removesimp @user)
@client.command()
#@commands.has_role('CAD Officer')
async def removesimp(ctx, mention, value=1):
    with open('points.json', 'r') as f:
        users = json.load(f)
    for user in ctx.message.mentions:
        tagid = str(ctx.message.mentions[0].id)
        username = ctx.message.mentions[0].mention
        await update_data(users, tagid)
        await remove_point(users, tagid, value)
        await ctx.send(f'{value} point was removed from {username}\'s simp score, they now have {users[tagid]["points"]} simp points.')
    with open('points.json', 'w') as f:
        json.dump(users, f)
#lists all the commands
#command is (;commands)
@client.command()
#@commands.has_role('CAD Officer')
async def commands(ctx):
    await ctx.send("Commands:\n\nsimp\nadds 1 or more simp points to the user tagged with an infraction\ncall example = (;simp @user 1 you are beautiful m'lady)\n1 is able to be replaced with any number and any text afterwards will be considered the infraction text\n\nchecksimp\nchecks the amount of simp points the tagged user has. This means if you want to check your own then you must tag yourself.\ncall example = (;checksimp @user)\n\nremovesimp\nremoves 1 simp point from the tagged user\ncall example = (;removesimp @user)\n\ncommands\npulls this message up\ncall example = (;commands)\n")

#functions
async def update_data(users, tagid):
    if not tagid in users:
        users[tagid] = {}
        users[tagid]['points'] = 0
        users[tagid]['simp level'] = "Normal User"

async def add_point(users, tagid, value):
    users[tagid]['points'] += value
    if tagid in users:
        if users[tagid]['points'] < 3:
            users[tagid]['simp level'] = "Normal User"
        elif users[tagid]['points'] >= 3 and users[tagid]['points'] < 6:
            users[tagid]['simp level'] = "Convincted Simp"
        elif users[tagid]['points'] >= 6 and users[tagid]['points'] < 9:
            users[tagid]['simp level'] = "High-Level Simp"
        elif users[tagid]['points'] >= 9 and users[tagid]['points'] < 12:
            users[tagid]['simp level'] = "Malfeasant Simp"
        elif users[tagid]['points'] >= 12 and users[tagid]['points'] < 15:
            users[tagid]['simp level'] = "Toesucker Simp"
        elif users[tagid]['points'] >= 15 and users[tagid]['points'] < 30:
            users[tagid]['simp level'] = "Cocknipples"
        elif users[tagid]['points'] >= 30:
            users[tagid]['simp level'] = "Demi-Male"

async def remove_point(users, tagid, value):
    users[tagid]['points'] -= value

async def points_message(users, tagid, message, value, infraction, channel, start_level):
    channel = client.get_channel(channel)
    tagidint = int(tagid)
    user = client.get_user(tagidint)
    if (value >= 3):
        await channel.send(f"{message.mentions[0].mention} has committed a __**felony**__ on account of \"{infraction}\" and recieved {value} points. Their current rank is __***{users[tagid]['simp level']}***__ for a total points of {users[tagid]['points']}")
    else:
        await user.send(f"You have committed a __**misdemeanor**__ on account of \"{infraction}\" and recieved {value} points. Your current rank is __***{users[tagid]['simp level']}***__ for a total points of {users[tagid]['points']}")
    quotes = [
        'Oh ye of little faith, the path chosen is a long one fraught with trials and tribulations, the only guarantee heartache. You may however still turn back, still have a shot at redemption.\nVenlock 2:33',
        'I mean really\nPorgis 1:1',
        'Let not sin therefore reign in your mortal body, to make you obey its passions.\nRomans 6:12',
        'Whoever loves pleasure will be a poor man; he who loves wine and oil will not be rich.\nProverbs 21:17',
        'Jesus answered them, “Truly, truly, I say to you, everyone who commits sin is a slave to sin.\nJohn, 8:34',
        'But I tell you that anyone who looks at a woman lustfully has already committed adultery with her in his heart.\nMatthew 5:28',
        'You say, “Food for the stomach and the stomach for food, and God will destroy them both.” The body, however, is not meant for sexual immorality but for the Lord, and the Lord for the body.\nCorinthians 6:13',
        'Flee the evil desires of youth and pursue righteousness, faith, love and peace, along with those who call on the Lord out of a pure heart.\nTimothy 2:22',
        'So I say, walk by the Spirit, and you will not gratify the desires of the flesh.\nGalatians 5:16',
        '"...but each person is tempted when they are dragged away by their own evil desire and enticed. Then, after desire has conceived, it gives birth to sin; and sin, when it is full-grown, gives birth to death.\nJames 1:14-15',
        '"Do not lust in your heart after her beauty or let her captivate you with her eyes."\nProverbs 6:25',
        '"I have made a covenant with my eyes; How then could I gaze at a virgin?"\nJob 31:1']
    quote = random.choice(quotes)
    if start_level != users[tagid]['simp level']:
        await channel.send(
            f"{message.mentions[0].mention} has leveled up from a {start_level} to a {users[tagid]['simp level']}\n\n{quote} ")



client.run(token)
