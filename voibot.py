#! /usr/bin/python3

import os
import random
import dotenv
import discord
import asyncio

client = discord.Client(
    intents=discord.Intents(
        members=True,
        messages=True,
        message_content=True,
        guilds=True,
    ),
)

xlate_table = {}
with open(os.path.join(os.path.dirname(__file__), "xlate")) as f:
    for line in f:
        xlate_table[line[0]] = line[2:-1]

def xlate(s):
    s = list(s)
    for i in range(len(s)):
        c = s[i].upper()
        if c not in xlate_table:
            continue
        s[i] = random.choice(xlate_table[c])
    return "".join(s)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    trigger = "!voibot "
    content = message.content
    if content.startswith(trigger):
        print(f"Summon message on channel {message.channel.name}")
        response = xlate(content[len(trigger):])
        await message.channel.send(response)

@client.event
async def on_member_join(member):
    print(f"New member {member.display_name}")
    await member.edit(nick=xlate(member.display_name))

async def main():
    dotenv.load_dotenv()
    token = os.getenv('DISCORD_TOKEN_VOIBOT')
    await client.start(token)


if __name__ == "__main__":
    all_tasks = [
        main(),
    ]
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*all_tasks))
