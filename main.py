import discord
import os
import requests
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
from urllib.parse import urlencode

client = discord.Client()
load_dotenv()
time_format = "%Y-%m-%dT%H:%M:%S"
default_delta=24

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} {client.user.id}')

async def get_contests(payload):
    start_time = datetime.now().strftime(time_format)
    end_time = datetime.now() + timedelta(days=payload['delta'])
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
        if payload['website'] in contest['href']:
            contests['upcoming'].append(contest)
    return contests

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    
    if message.content.startswith('$list'):
        payload = message.content[len('$list'):].strip().split(' ')
        print(payload, len(payload))
        if len(payload) == 1 and payload[0] == '':
            await message.channel.send('Pass a website and a time delta to find the list of upcoming contests...')
        else:
            website = payload[0]
            if len(payload) >= 2:
                delta = payload[1]
            else:
                delta = default_delta
            res = await get_contests({'website' : website, 'delta' : float(delta)/24})
            if len(res['upcoming']) == 0:
                desc = f'There are no upcoming in the next {delta} hours...'
            else:
                desc = f'Contests on {website} in the next {delta} hours'
            embed = discord.Embed(
                title = f'Upcoming {website} contests',
                description = desc,
                color = discord.Color.dark_blue()
            )
            for contest in res['upcoming']:
                desc = f'> {contest["href"]}'
                embed.add_field(name=contest['event'], value=desc, inline=False)
            await message.channel.send(embed=embed)

client.run(os.getenv('TOKEN'))