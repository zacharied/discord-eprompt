#!/usr/bin/env python3.7

import discord
from discord.ext import commands

from discord_eprompt import react_prompt_response, ReactPromptPreset

import json
import sys
from os import path

CONFIG_PATH = 'example.json'

class TestBot(commands.Bot):
    def __init__(self, guild_id, *args, **kwargs):
        super().__init__(command_prefix='!', *args, **kwargs)
        self.guild_id = guild_id

    async def start_prompt(self):
        print('Starting reaction prompt.')
        message = await self.channel.send('This is a single-use reaction prompt.')
        response = await react_prompt_response(self, self.guild.owner, message, preset=ReactPromptPreset.DIGITS)
        print(f'User responeded with "{response}".')
        await self.channel.send(f'You chose "{response}".')

        print('Starting persistent reaction prompt.')
        message = await self.channel.send('This is persistent: choose a number 0-9. Then choose a number 0-4.')
        response1 = await react_prompt_response(self, self.guild.owner, message, persist_message=True, reacts={f'{i}\u20e3': i for i in range(10)})
        response2 = await react_prompt_response(self, self.guild.owner, message, persist_message=False, reacts={f'{i}\u20e3': i for i in range(5)})
        await self.channel.send(f'You chose {response1} and then {response2}.')
    
    async def on_ready(self):
        print('Connected to server.')
        self.guild = self.get_guild(self.guild_id)
        self.channel = self.guild.text_channels[0]
        print(f'Using channel "{self.channel.name}".')
        await self.start_prompt()

if __name__ == '__main__':
    if not path.exists(CONFIG_PATH):
        print(f'No config file found. Please copy "{CONFIG_PATH}.template" to "{CONFIG_PATH}" and edit the values within.', file=sys.stderr)
        sys.exit(1)

    with open(CONFIG_PATH) as config_file:
        config = json.loads(config_file.read())
        bot = TestBot(config["guild"])
        bot.run(config["token"])
