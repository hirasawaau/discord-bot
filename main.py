import os

from difflib import get_close_matches

from discord.ext import commands
from dotenv import load_dotenv
from src.poker.welcome import get_players
from src.poker.poker import get_random_cards, send_card_msg
from src.poker.poker import three_middle_card_msg, loop_pass_bet_fold
from src.poker.help import command_list

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="$")


@bot.command(name="hello")
async def nine_nine(ctx):
    channel = bot.get_channel(ctx.channel.id)
    message_id = channel.last_message_id
    await ctx.send("HI :heart:")


@bot.command(name="poker")
async def poker(ctx):
    players = await get_players(bot, ctx)
    if players is None:
        return
    player_cards, middle_cards = get_random_cards(players)
    print(middle_cards)
    print(player_cards)
    await send_card_msg(players, player_cards)
    await three_middle_card_msg(middle_cards, ctx)
    players_left, player_cards_left = await loop_pass_bet_fold(
        players, player_cards, bot, ctx
    )


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.replace("$", "") not in command_list:
        similar_commands = get_close_matches(message.content, command_list)
        try:
            await message.channel.send(f"Syntax: ${similar_commands[0]}")
        except:
            pass


bot.run(TOKEN)