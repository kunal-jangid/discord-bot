# Modules and stuff
import os
import random
import discord
import asyncio
from discord import Spotify
import datetime
import youtube_dl
from pyrandmeme import *
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from keep_alive import keep_alive
from discord_webhook import DiscordWebhook
from discordTogether import DiscordTogether


# Environment variables and calling modules
keep_alive()
TOKEN = os.environ['token']
weburl = os.environ['url']
noNe = os.environ['dm-er']

# 2
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='&', intents=intents)
slash = SlashCommand(bot, sync_commands=True)
togetherControl = DiscordTogether(bot)


# Bot events
@bot.event 
async def on_ready():
  print('Connected to bot: {}'.format(bot.user.name))
  print('Bot ID: {}'.format(bot.user.id))

@bot.event
async def on_message(message):
  channel = bot.get_channel(860588755202211921)
  if message.guild is None and message.author != bot.user:
    embed = discord.Embed(title=" ", description=" ")
    embed.add_field(name='DM by '+message.author.name, value=message.content)
    await channel.send(embed=embed)
  await bot.process_commands(message)

  
# Bot commands from here

@bot.command(name="ping")
async def ping(ctx):
	embed = discord.Embed(title=" ", color=708090)
	embed.add_field(
	    name="Ping Pong!",
	    value=f'Ping pong,you are recieving good {bot.latency *1000}ms ping.')
	await ctx.send(embed=embed)


@slash.slash(name="Calculate", description="Basic calculating like addition, substraction, exponential multiplication and much more")
async def calc(ctx, num1, operation, num2):
	"""Operations available - +(addition), +(subtraction), *(multiplication), /(division), //(floor division), **(exponential values) and %(modulus)."""
	var = (num1 + operation + num2)
	await ctx.send(f'{var} = {eval(var)}')


@bot.command(pass_context=True)
async def purge(ctx, amount=1):
	channel = ctx.message.channel
	messages = []
	async for message in channel.history(limit=amount + 1):
		messages.append(message)

	await channel.delete_messages(messages)
	await ctx.send(
	    f'{amount} messages have been purged by {ctx.message.author.mention}',
	    delete_after=1)


@bot.command(name='repeat')
async def repeat(stx, num, *args):
	await stx.message.delete()
	for i in range(int(num)):
		await stx.send(" ".join(args[:]))


@bot.command()
async def create_channel(stx, arg):
	guild = stx.guild
	await guild.create_text_channel(arg)


@bot.command()
async def webhook(stx, *args):
	await stx.message.delete()
	webhook = DiscordWebhook(url=weburl, content=(" ".join(args[:])))
	response = webhook.execute()
	await stx.send(response)


@bot.command()
async def nick(ctx, member: discord.Member, *arg):
	await member.edit(nick=" ".join(arg[:]))
	embed = discord.Embed(title="Nickname Modification",
	                      description=" ",
	                      color=708090)
	embed.add_field(name=f"{member.name}",
	                value="Your name has been successfully changed.")
	await ctx.send(embed=embed)


@bot.command()
async def react(ctx, emoji, idd):
	message = ctx.channel.fetch_message(idd)
	await message.add_reaction(emoji)


@bot.command()
async def spotify(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author
		pass
	if user.activities:
		for activity in user.activities:
			if isinstance(activity, Spotify):
				embed = discord.Embed(title=f"{user.name}'s Spotify",
				                      description="Listening to {}".format(
				                          activity.title),
				                      color=708090)
				embed.set_thumbnail(url=activity.album_cover_url)
				embed.add_field(name="Artist", value=activity.artist)
				embed.add_field(name="Album", value=activity.album)
				embed.set_footer(text="Song started at {}".format(
				    activity.created_at.strftime("%H:%M")))
				await ctx.send(embed=embed)


#studycommand
@bot.command()
async def studying(ctx, seconds, *arg):
	await ctx.message.delete()

	try:
		secondint = int(seconds)
		if secondint > 7200:
		  await ctx.send(
			    "I dont think im allowed to do go above 2 hours/7200 seconds.")
			
		if secondint <= 0:
			await ctx.send("I dont think im allowed to do negatives =_=")
		message = await ctx.send(" ".join(arg[:]) +
		                         " timer for {ctx.author.name}: {seconds}")
		while True:
			secondint -= 1
			if secondint == 0:
				await message.edit(content=" ".join(arg[:])+" timer ended!")
				break
			await message.edit(content=" ".join(arg[:]) +
			                   f" timer for {ctx.author.name}: {secondint}")
			await asyncio.sleep(1)
		await ctx.send(f"{ctx.author.mention} congrats, your timer just ended!")
	except ValueError:
		await ctx.send("Must be a number!")

@slash.slash(name="Avatar", description="Displays the pfp of mentioned user.")
async def avatar(ctx, member: discord.Member):
  embed = discord.Embed(title="Avatar", description=member.display_name)
  embed.set_image(url=member.avatar_url)
  await ctx.send(embed=embed)

@bot.command()
async def time(stx, seconds=1000000):
	await stx.message.delete()
	while True:
		now = str(datetime.datetime.now())
		sep_date_time = now.split(' ')
		n_date = sep_date_time[0]
		n_time = sep_date_time[1]
		sep_time = n_time.split(':')
		current_time = "Time => " + sep_time[0] + ":" + sep_time[
		    1] + ":" + sep_time[2]
		samay = await stx.send(current_time)
		await stx.send("Date => " + n_date)

		for i in range(int(seconds)):
			now = str(datetime.datetime.now())

			sep_date_time = now.split(' ')
			n_time = sep_date_time[1]
			sep_time = n_time.split(':')
			current_time = "Time => " + sep_time[0] + ":" + sep_time[
			    1] + ":" + sep_time[2]

			await samay.edit(content=current_time)
			await asyncio.sleep(1)

		break


@slash.slash(name="Reddit", description="Posts random image from given subreddit's hot lists")
async def reddit(ctx,subreddit='wholesome'):
  """posts random reddit post with given argument"""
  await ctx.send(embed=await pyrandmeme(subreddit))


Sq_list = [
    " gently squeezes ", " shares some hugs with ",
    " spreads a little, yes just a little love with ", " gently hugs ",
    " sends a free hug pass to ", " crash lands into ",
    "crashes (too much adreneline, I guess) directly into ",
    " share a gently squeeze with "
]


@slash.slash(name="Squeeze",description="Hug the mentioned")
async def squeeze(stx, member: discord.Member):
	m = len(Sq_list)
	n = random.randint(0, m - 1)
	s = f"{stx.author.mention}" + Sq_list[n] + f"{member.mention}"
	await stx.send(s)


@bot.command()
async def scream(stx, arg, num):
	await asyncio.sleep(1)
	await stx.message.delete()
	try:
		a = arg * int(num)
		await stx.send(a)
	except:
		wa = await stx.send("Give correct values smh")
		await wa.delete()

@bot.command()
async def status(stx,*args):
  await stx.message.delete()
  act = " ".join(args[:])
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name= act))


@bot.command()
async def members(ctx):
  embed = discord.Embed(title="Member List", description=" ", color = 708090)
  n = 0
  for i in ctx.guild.members:
    n += 1
    embed.add_field(name="Member "+str(n)+":", value=i.name)
  await ctx.send(embed=embed)


bot.run(TOKEN)
client.run(TOKEN)
