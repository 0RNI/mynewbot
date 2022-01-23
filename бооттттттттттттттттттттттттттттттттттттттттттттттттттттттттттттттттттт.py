import discord

from discord.ext import commands
import datetime
from discord.utils import get

import requests

import io



PREFIX = '!'
bad_words = ['кик', 'флуд', 'спам', 'блять', 'сука', 'писька', 'уёбище', 'канава', 'бомж', 'гей', 'пидр', 'пидрила', 'пиздюк', 'пизда', 'хуй', 'член', 'блядина', 'тупой', 'flud', 'gey', 'spam']

client= commands.Bot(command_prefix= PREFIX)
client.remove_command('help')

@client.event

async def on_ready():
    print('бот зарегался ёпт=)')

    await client.change_presence(status= discord.Status.do_not_disturb, activity=discord.Game("БЕБРА"))

@client.event

async def on_member_join(member):
    channel = client.get_channel(934478717856665683)

    role = discord.utils.get(member.guild.roles, id = 934767652310745108)

    await member.add_roles(role)
    await channel.send(embed = discord.Embed(discription = f'Пользователь ``{member.name}``, присоеденился к нам!', color=0x0c0c0c))

@client.event
async def on_message(message):
    await client.process_commands(message)

    msg = message.content.lower()

    if msg in bad_words:
        await message.delete()
        await message.author.send(f'{message.author.name}, не надо такое писать! А то по попе дам:< !')

@client.command(pass_context = True)
@commands.has_permissions(administrator= True)

async def clear(ctx, amount= 100):
    await ctx.channel.purge(limit = amount)

@client.command(pass_context= True)

async def hello(ctx, amount= 1):
    await ctx.channel.purge(limit= amount)

    author = ctx.message.author
    await ctx.send(f'Hello {author.mention}')

@client.command(pass_context= True)
@commands.has_permissions(administrator= True)

async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit= 1)

    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} был кикнут за плохое повидение на сервере!')

@client.command(pass_context = True)
@commands.has_permissions(administrator= True)

async def ban(ctx, member: discord.Member, *, reason = None):
    emb=discord.Embed(title='Ban', colour= discord.Color.purple(),)
    await ctx.channel.purge(limit= 1)

    await member.ban(reason=reason)

    emb.set_author(name=member.name, icon_url = member.avatar_url)
    emb.add_field(name= 'Бан участника', value = 'Участник забанен : {}'.format(member.mention))
    emb.set_footer(text= 'Был забанен администратором {}'.format((ctx.author.name), icon_url= ctx.author.avatar_url))

    await ctx.send(embed = emb)

    #await ctx.send(f'{member.mention} забанен=)')

@client.command(pass_context = True)
@commands.has_permissions(administrator= True)

async def unban(ctx, *, member):
    await ctx.channel.purge(limit = 1)

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban(user)
        await ctx.send(f'пользователль разбанен {user.mention}')

        return

@client.command(pass_context = True)

async def help(ctx):
    await ctx.channel.purge(limit = 1)

    emb = discord.Embed(title='Навгация по командам')

    emb.add_field(name='{}clear'.format(PREFIX), value= 'очищяет всё на своём пути')
    emb.add_field(name='{}kick'.format(PREFIX), value='выбрасывание игрока с сервера=)')
    emb.add_field(name='{}ban'.format(PREFIX), value='БААААААААН!')
    emb.add_field(name='{}unban'.format(PREFIX), value='РАААААААААААЗЗЗ БААААААААН')

    await ctx.send(embed= emb)

@client.command(pass_context = True)
@commands.has_permissions(administrator= True)

async def youtube(ctx):
    emb = discord.Embed(title = 'Ютубчик=)', descriptoin = 'посмотри видосики)', colour= discord.Color.red(), url= 'https://www.youtube.com')

    emb.set_author(name = client.user.name, icon_url= client.user.avatar_url)
    emb.set_footer(text = 'Спасибо за использование нашего бота!', icon_url=ctx.author.avatar_url)
    #emb.set_image(url='https://www.actualidadiphone.com/wp-content/uploads/2015/07/Youtube.jpg')
    emb.set_thumbnail(url='https://www.actualidadiphone.com/wp-content/uploads/2015/07/Youtube.jpg')

    now_date = datetime.datetime.now()

    emb.add_field(name = 'Time', value= 'Time : {}'.format(now_date))

    await ctx.send(embed= emb)

@client.command()
@commands.has_permissions(administrator= True)

async def user_mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')

    await member.add_roles(mute_role)
    await ctx.send(f'У {member.mention}, ограничение чата, за нарушение прав!')

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоеденился к каналу: {channel}')

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот отключился от канала: {channel}')


@client.command()
async def send_a(ctx):
    await ctx.author.send('приветик!')


@client.command()
async def send_m(ctx, member: discord.Member):
    await member.send(f'{member.name} привет, удачи на нашем серере!')

# Connect

token = open('token.txt', 'r').readline()

client.run(token)