#Discord Cleverbotbot
import discord
from discord.ext import commands
import random
from datetime import datetime
from gosu_gamers.gg_match import Dota2MatchScraper
bot = commands.Bot(command_prefix='?', description='2clever4you')

starttime = datetime.now()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(starttime)
    print('------')

@bot.command()
async def uptime():
    await bot.say(datetime.now() - starttime)

@bot.command(pass_context=True)
async def server(ctx):
    await bot.say(ctx.message.server)
    await bot.say(ctx.message.server.id)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command()
async def repeat(times : int, content : str):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)


@bot.command(pass_context=True)
async def clear(ctx):
    channel = ctx.message.channel
    to_delete = list()
    for message in bot.messages:
        if message.channel == channel:
            print(message.author)
            if message.author.name == 'cleverbotbot':
                to_delete.append(message)
            elif message.content[0] == '?' and len(message.content) > 2:
                to_delete.append(message)
    await bot.delete_messages(to_delete)

@bot.command()
async def dotaticker():
    match_scraper = Dota2MatchScraper()

    live_matches = match_scraper.find_live_matches()
    for live_match in live_matches:
        live_match.live_in = 'Live'

    upcoming_matches = match_scraper.find_upcoming_matches()

    games_list = live_matches + upcoming_matches

    for game in games_list:
        string = '{} in: {}\n {}'.format(game.simple_title, game.live_in, game.url)
        await bot.say(string)

def is_bot_post(message):
    return message.author.name == 'cleverbotbot' or (message.content[0] == '?' and len(message.content) > 2)


@bot.event
async def on_message(message):
     await bot.process_commands(message)

bot.run('your token here')
