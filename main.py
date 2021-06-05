import discord
import os
from discord.errors import HTTPException
import requests
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
from urllib.parse import urlencode

client = discord.Client()
load_dotenv()
time_format = "%Y-%m-%dT%H:%M:%S"

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} {client.user.id}')

async def get_contests(website):
    start_time = datetime.now().strftime(time_format)
    end_time = datetime.now() + timedelta(days=1)
    end_time = end_time.strftime(time_format)
    base = 'https://clist.by/api/v2/contest/?'
    params = {'username' : os.getenv("USERNAME"), 'api_key' : os.getenv("API_KEY"), 'order_by' : 'start'}
    params['start__gte'] = start_time
    params['start__lte'] = end_time
    url = base + urlencode(params)
    contests = {'upcoming': []}
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    if response.status_code != 200:
        return contests
    json = response.json()
    for contest in json['objects']:
        if website in contest['href']:
            contests['upcoming'].append(contest)
    return contests

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    
    if message.content.startswith('$list'):
        site = message.content[len('$list'):].strip().lower()
        res = {}
        embed = discord.Embed(
            title=f'Upcoming {site} contests',
            description=f'Contests that will be held on {site} in the next 24 hours',
            color=discord.Color.dark_blue()
        )
        res = await get_contests(site)
        for contest in res['upcoming']:
            desc = f'> {contest["href"]}'
            embed.add_field(name=contest['event'], value=desc, inline=False)
        await message.channel.send(embed=embed)

client.run(os.getenv('TOKEN'))