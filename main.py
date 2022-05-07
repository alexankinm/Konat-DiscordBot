import discord
from discord.ext import commands
import os
import datetime
from keep_alive import keep_alive
import time
import requests
import json

from urllib import parse, request
from threading import Thread
import re

prefix = '?'
version = 'Версия 1.0'

bot = commands.Bot(
  command_prefix=prefix,
  description="Команда Help",
	fetch_offline_members = True,
	guild_subscriptions = True,
	allowed_mentions = discord.AllowedMentions.all(),
  intents = discord.Intents.all()
)
bot.remove_command('help')

#@bot.event
#async def on_message(msg):
#	msgx = msg.content.lower()
#print(f'{msg.guild.name} | {msg.author.name}#{msg.author.discriminator} | {msg.author.id}: {msgx}')


# Events
@bot.event
async def on_ready():
    guilds = await bot.fetch_guilds(limit=None).flatten()
    await bot.change_presence(activity=discord.Activity(
        name=f'{prefix}help | {len(guilds)} серверов',
        type=discord.ActivityType.watching))
    #  await bot.change_presence(activity=discord.Game(name="{prefix}help | {len(guilds)} серверов"))
    #  print(f"Бот {bot.user} успешно запущен.")
    #  print(f'[Discord] Bot Started: {bot.user.name}#{bot.user.discriminator} | {bot.user.id}')
    print(f"Beep beep! 🤖")
    print(f" ")
    servers = list(bot.guilds)
    print(" " + str(len(bot.guilds)) + " 💖")
    for guild in bot.guilds:
        print(f" - {guild.name} | {guild.id}")


@bot.event
async def on_server_join(server):
    await bot.change_presence(activity=discord.Game(
        name="{prefix}help | {len(guilds)} серверов"))


@bot.event
async def on_button_click(interaction):
    if interaction.responded:
        return
    else:
        embederror = discord.Embed(
            title=f'Взаимодействие недоступно',
            description=
            f'Данное взаимодействие недоступно. Перезапустите команду',
            colour=discord.Colour.from_rgb(255, 0, 0))
        await interaction.send(embed=embederror)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embederror = discord.Embed(
            title=f'Неправильная команда',
            description=
            f'Команда не найдена, проверь, ты её правильно ввёл, и повтори попытку',
            colour=discord.Colour.from_rgb(255, 71, 71))
        await ctx.send(embed=embederror)
        pass
    elif isinstance(error, commands.CommandOnCooldown):
        embederror = discord.Embed(
            title=f'Ограничение',
            description=
            f'Обнаружен слишком частый ввод одной команды, повтори через { error.retry_after }',
            colour=discord.Colour.from_rgb(255, 71, 71))
        await ctx.send(embed=embederror)
        pass
    else:
        print(error)

        report_errror_channel = bot.get_channel(963854979993587802)
        await report_errror_channel.send(f'```{error}```')

        embederror = discord.Embed(
            title=f'Упс, что-то сломалось!',
            description=
            f'Похоже, что-то сломалось опять! Но не волнуйтесь. Ошибка уже была отправлена и будет скоро исправлена',
            colour=discord.Colour.from_rgb(255, 71, 71))
        await ctx.send(embed=embederror)
        pass


@bot.command()
async def ping(ctx):
    await ctx.send(f'Я тут! Мой пинг: {bot.latency*1000}ms')


@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)


@bot.command()
async def server_info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}",
                          description="Информация о сервере",
                          timestamp=datetime.datetime.utcnow(),
                          color=discord.Color.blue())
    embed.add_field(name="Сервер создан",
                    value=f"{ctx.guild.created_at}",
                    inline=False)
    embed.add_field(name="Владелец сервера",
                    value=f"{ctx.guild.owner}",
                    inline=False)
    embed.add_field(name="Регион сервера",
                    value=f"{ctx.guild.region}",
                    inline=False)
    embed.add_field(name="Участников на сервере",
                    value=f"{ctx.guild.member_count}",
                    inline=False)
    embed.add_field(name="ID сервера", value=f"{ctx.guild.id}", inline=False)
    #embed.set_image(url=ctx.guild.icon)

    await ctx.send(embed=embed)

@bot.command()
async def bot_info(ctx):
    embed = discord.Embed(title=f"Konat",
                          description="Информация о боте",
                          timestamp=datetime.datetime.utcnow(),
                          color=discord.Color.blue())
    embed.add_field(name="Префикс", value=f"{prefix}", inline=False)
    embed.add_field(name="Количество серверов",
                    value=f"{len(bot.guilds)}",
                    inline=False)
    embed.add_field(name="Создатель", value=f"Esty88#5009")
    embed.add_field(name="Ещё Разработчики", value=f"ДраконОгонь 🐲#8392")

    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' +
                                   query_string)
    # print(html_content.read().decode())
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})',
                                html_content.read().decode())
    print(search_results)
    # I will put just the first result, you can loop the response to show more results
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, user_id, userName: discord.User):
    user = ctx.message.author
    role = discord.utils.get(user.server.roles, name="•┆๑💀๑∴Мьют∴")
    await ctx.author.add_roles(user, role)


@bot.command(brief='Банить участников сервера')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(color=discord.Color.blue(), title='Ban')
    embed.add_field(
        name=f'Участник *{ member }* успешно забанен на этом сервеве. ',
        value=f'Причина: { reason }',
        inline=False)
    await ctx.send(embed=embed)


@bot.command(brief='Кикать участников с сервера')
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
    if not reason:
        await user.kick()
        embed = discord.Embed(color=discord.Color.blue, title='Кик')
        embed.add_field(name=f'Участник *{ user }* успешно кикнут с сервера. ',
                        value=f'Причина: причина не указана',
                        inline=False)
        await ctx.send(embed=embed)
    else:
        await user.kick(reason=reason)
        embed = discord.Embed(color=discord.Color.blue(), title='Кик')
        embed.add_field(name=f'Участник *{ user }* успешно кикнут с сервера. ',
                        value=f'Причина: { reason }',
                        inline=False)
        await ctx.send(embed=embed)


@bot.command(brief="Очистка")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number: int):
    await ctx.channel.purge(limit=number)
    embed = discord.Embed(color=discord.Color.blue(),
                          title='Канал успешно очищен')
    await ctx.send(embed=embed)


#_______________________КОМАНДА help_______________________
@bot.command()
async def help(ctx, comname: str = None):
    embed = discord.Embed(
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow(),
        title="Команды **Konat**",
        description=
        f"**<:clipboard:920714709932593182> Основное**\n`{prefix}help` - все команды бота\n`{prefix}invite` - добавить бота\n**<:shield:920714733278077010> Модерация**\n`{prefix}clear` - очистка сообщений\n`{prefix}mute` - заглушить пользователя\n`{prefix}unmute` - размутить пользователя\n`{prefix}kick` - выгнать пользователя\n`{prefix}ban` - забанить пользователя\n`{prefix}niсk` - сменить ник пользователю\n**<:wrench:920715659481075734> Утилиты**\n`{prefix}server_info` - информация о сервере\n`{prefix}bot_info` - информация о боте\n`{prefix}sum` - прибавление чисел\n`{prefix}avatar` - аватар пользователя\n**<:performing_arts:972614168559644692> Ролевые Игры**\n`{prefix}hug` - обнять\n`{prefix}wink` - подмигнуть\n`{prefix}pat` - погладить\n<:butterfly:972620588491358288> Изображения\n`{prefix}cat` - случайный котик\n`{prefix}dog` - случайный пёс\n`{prefix}fox` - рандомная лиса\n`{prefix}bird` - рандомная птица",
    )
    embed.set_thumbnail(url=bot.user.avatar_url)

    if comname == "info":
        embinf = discord.Embed(
            title='`Информация о команде >info`',
            description='**Описание:**\nИнформация о данном боте',
            color=0xff9900)
        embinf.set_thumbnail(url=bot.user.avatar_url)
    else:
        await ctx.reply(embed=embed)


@bot.command()
async def create_invites(ctx):
    for guild in bot.guilds:
        for c in guild.text_channels:
            if c.permissions_for(guild.me).create_instant_invite:
                invite = await c.create_invite()
                print(invite)
                break


@bot.command()
async def invite(ctx):
    await ctx.author.send(
        'Пригласить меня на свой сервер: https://discord.com/api/oauth2/authorize?client_id=939606679224459334&permissions=8&scope=bot'
    )

    embed = discord.Embed(
        color=discord.Color.blue(),
        title='Я тебе отправил ссылку в личные сообщения',
        description="Надеюсь ты меня добавишь на свой сервер :3",
        timestamp=datetime.datetime.utcnow())
    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow(),
        title=f"Аватар участника - {member.name}",
        description=f"[Нажмите что бы скачать аватар]({member.avatar_url})")
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content == "<@939606679224459334>":
        await message.channel.send(f'Мой префикс на этом сервере: ``{prefix}``'
                                   )


@bot.command(brief="Управление ботом")
@commands.is_owner()
async def db_manage(ctx):
    await ctx.send("Панель управления ботом",
                   components=[
                       Button(label="Выключить",
                              custom_id="Shutdown",
                              style=ButtonStyle.red),
                       Button(label="Перезапустить",
                              custom_id="Restart",
                              style=ButtonStyle.green),
                       Button(label="Обновить Статус",
                              custom_id="Update Status",
                              style=ButtonStyle.blue)
                   ])
    interaction = await bot.wait_for("button_click")

    if interaction.custom_id == 'Shutdown':
        await bot.change_presence(status=discord.Status.idle,
                                  activity=discord.Game(f"Shutdowning..."))
        await bot.close()
    if interaction.custom_id == 'Restart':
        await ctx.send("Перезапуск")
        os.system("python main.py")
        await ctx.send("Ошибка перезапуска")
    if interaction.custom_id == 'Update Status':
        guilds = await bot.fetch_guilds(limit=None).flatten()
        await bot.change_presence(activity=discord.Activity(
            name=f'{prefix}help | {len(guilds)} серверов',
            type=discord.ActivityType.watching))
        await interaction.respond("Статус обновлён")


@bot.command()
async def hug_dragon(ctx, hugMention: discord.Member):
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)

    embed = discord.Embed(
        color=0xff9900,
        title=f'{ctx.author.mention} обнял {hugMention.mention}')
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)






@bot.command()
async def hug(ctx, member: discord.Member):
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)

    embed = discord.Embed(title="Объятия! 💖", description="**{1}** обнял **{0}**!".format(member.name, ctx.message.author.name), color = discord.Color.blue(), timestamp=datetime.datetime.utcnow())

    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)



@bot.command()
async def wink(ctx, member: discord.Member):
    response = requests.get('https://some-random-api.ml/animu/wink')
    json_data = json.loads(response.text)

    embed = discord.Embed(description="**{1}** подмигнул **{0}**!".format(member.name, ctx.message.author.name), color = discord.Color.blue(), timestamp=datetime.datetime.utcnow())

    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)




@bot.command()
async def pat(ctx, member: discord.Member):
    response = requests.get('https://some-random-api.ml/animu/pat')
    json_data = json.loads(response.text)

    embed = discord.Embed(description="**{1}** погладил **{0}**!".format(member.name, ctx.message.author.name), color = discord.Color.blue(), timestamp=datetime.datetime.utcnow())

    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)




@bot.command()
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat')
    json_data = json.loads(response.text)

    embed = discord.Embed(title = "Случайный котик 🐱", color = discord.Color.blue(), timestamp=datetime.datetime.utcnow())

    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)



@bot.command()
async def dog(ctx):
    response = requests.get('https://some-random-api.ml/img/dog')
    json_data = json.loads(response.text)

    embed = discord.Embed(title = "Случайный пёс 🐶", color = discord.Color.blue(), timestamp=datetime.datetime.utcnow())

    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)


@bot.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox')
    json_data = json.loads(response.text)

    embed = discord.Embed(title = "Случайная лиса 🦊", color = discord.Color.blue(), timestamp=datetime.datetime.utcnow())

    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)


@bot.command()
async def bird(ctx):
    response = requests.get('https://some-random-api.ml/img/birb')
    json_data = json.loads(response.text)

    embed = discord.Embed(title = "Случайная птица 🐦", color = discord.Color.blue(), timestamp=datetime.datetime.utcnow())

    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)



bot.run(os.environ["bot_token"])
