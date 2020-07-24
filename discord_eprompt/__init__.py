import asyncio

import discord
from discord.ext import commands

from enum import Enum

from typing import Dict, Union

class ReactPromptPreset(Enum):
    """ Common sets of choices for prompts.

    A preset is defined as a dictionary with the keys being emoji to react with, and the values being a string 
    representation of the response.
    """

    YES_NO = {'\U0001F44D': 'yes', '\U0001F44E': 'no'}
    DIGITS = {f'{i}\u20e3': i for i in range(10)}

async def _on_prompt_reacted(prompt, bot, response:str, future):
    await prompt.message.delete()
    bot.remove_cog(prompt)
    
    future.set_result(response)

async def react_prompt_response(
        bot: commands.Bot,
        user: Union[discord.User, discord.Member],
        message: discord.Message,
        preset:ReactPromptPreset=None,
        reacts:Dict[str, str]=None
):
    """ Use a message as a reaction prompt and get the user's choice. 

    The bot will add the given reactions to the message and disallow anyone other than the specified user from reacting.
    This will return a string representation of the user's choice when the user clicks on a reaction.

    :param bot: The bot that will react to the message with the choices for the user.
    :param user: The user who is allowed to react.
    :param message: The message to use as the prompt.
    :param preset: The list of choices, defined as a preset by the library.
    :param reacts: The list of choices, defined as a dictionary in which the keys are the emoji to use as the reaction,
        and the values are what will be returned when that respective choice is selected.

    :return: The user's choice.
    """

    if preset is None and reacts is None:
        raise ValueError('either a preset or set of reactions must be defined')
    elif preset is not None and reacts is not None:
        raise ValueError('cannot have both a preset and set of reactions')

    if preset is not None:
        reacts = preset.value

    loop = asyncio.get_running_loop()
    future = loop.create_future()

    prompt = _ReactPrompt(bot, user, message, reacts, lambda response: _on_prompt_reacted(prompt, bot, response, future))
    await prompt.setup()

    return await future

class _ReactPrompt(commands.Cog):
    def __init__(self, bot: commands.Bot, user: discord.User, message: discord.Message, reacts: Dict[str, str], callback):
        self.bot = bot
        self.user = user
        self.message = message
        self.reacts = reacts
        self.callback = callback

        self.reactions_added = False

    async def setup(self):
        self.bot.add_cog(self)

        for react in self.reacts.keys():
            await self.message.add_reaction(react)
        self.reactions_added = True

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id != self.message.id:
            # Only act when the bound message is reacted to.
            return

        if user == self.bot.user:
            # Allow the bot to react with the choices.
            return

        if not self.reactions_added or \
                user != self.user or \
                str(reaction) not in self.reacts.keys():
            # Prevent user from making a choice before we've added all of them.
            # Also remove reactions from other users, or reactions that were not already made by the bot.
            await self.message.remove_reaction(reaction, user)
            return

        reaction_response = self.reacts[str(reaction)]
        await self.callback(reaction_response)
