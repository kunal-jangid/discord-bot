import aiohttp
import discord
import random2


async def pyrandmeme(x):
    pymeme = discord.Embed(title="A r/"+x+" post for you, thank me later :wink: ", color=708090)
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/'+x+'/new.json?sort=hot') as r:
            res = await r.json()
            pymeme.set_image(url=res['data']['children'][random2.randint(0, 15)]['data']['url'])
            return pymeme
        await pyrandmeme()
