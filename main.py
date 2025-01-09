import discord # Подключаем библиотеку
from discord.ext import commands

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='>', intents=intents)

# С помощью декоратора создаём первую команду
@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run('MTMyNjk5MTYwNjE1MDMzNjYyNg.Gp_H0Z.jAt6MUNQbOo2Hbrx-HMT1yDMqmwXdIqy2xh_wk')