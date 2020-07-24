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
        message = await self.channel.send('Hello world!')
        response = await react_prompt_response(self, self.guild.owner, message, preset=ReactPromptPreset.DIGITS)
        print(f'User responeded with "{response}".')
    
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
