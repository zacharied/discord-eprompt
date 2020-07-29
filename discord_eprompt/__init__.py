import asyncio
import string, random

import discord
from discord.ext import commands

from enum import Enum

from typing import Dict, Union

_COG_IDENTIFIER_LENGTH = 8

class ReactPromptPreset(Enum):
    """ Common sets of choices for prompts.

    A preset is defined as a dictionary with the keys being emoji to react with, and the values being a string 
    representation of the response.
    """

    YES_NO = {'\U0001F44D': 'yes', '\U0001F44E': 'no'}
    DIGITS = {f'{i}\u20e3': i for i in range(10)}

async def _on_prompt_reacted(prompt, bot, response:str, future):
    if not prompt.persist_message:
        await prompt.message.delete()

    bot.remove_cog(prompt.identifier)
    
    future.set_result(response)

async def react_prompt_response(
        bot: commands.Bot,
        user: Union[discord.User, discord.Member],
        message: discord.Message,
        preset:ReactPromptPreset=None,
        reacts:Dict[str, str]=None,
        persist_message:bool=False
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
    :param persist_message: Whether or not to keep the message after the user reacts to it. The default behavior is to
        delete the message upon user input.

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

    cls = _prompt_cog_generate()
    prompt = cls(bot, user, message, reacts, persist_message, lambda response: _on_prompt_reacted(prompt, bot, response, future))
    await prompt.setup()

    return await future

def _prompt_cog_generate():
    """ Create a new ReactPrompt class with a randomized identifier.

    The random identifier is required because while calls to `add_cog` take a cog as a parameter, removing the cog takes a string. By default, the
     string value is just the name of the class. It can be changed by setting the cog's meta info, done here via the `name` kwarg. However, this will
     still fail in the even that more than one instance of the ReactPrompt cog is added to the bot at once, since all instances of the cog will have
     the same name and thus cannot be distinguished during the `remove_cog` call. The solution here is to dynamically generate the ReactPrompt class
     with a new `name` parameter each time we add it to the bot. We store the value of the name in the prompt as well, and then reference that when
     we need to remove the cog.
    """

    cog_identifier = ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    class ReactPrompt(commands.Cog, name=cog_identifier):
        def __init__(self, bot: commands.Bot, user: discord.User, message: discord.Message, reacts: Dict[str, str], persist_message: bool, callback):
            self.bot = bot
            self.user = user
            self.message = message
            self.reacts = reacts
            self.persist_message = persist_message
            self.callback = callback
            self.identifier = cog_identifier

            self.reactions_added = False

        async def setup(self):
            self.bot.add_cog(self)

            # Reactions are not added to the `message` object itself since it is cached from when we
            #  first sent it. We need to fetch the message to get its updated state.
            cache_message = await self.message.channel.fetch_message(self.message.id)

            for react in cache_message.reactions:
                # Remove any reactions made before we attached to this message.
                if react.emoji not in self.reacts.keys():
                    # Remove reactions not in our choices.
                    await react.clear()
                    continue
                
                async for user in react.users():
                    # Remove reactions that *are* in our choices but aren't from the bot.
                    if user != self.bot.user:
                        await react.remove(user)

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

    return ReactPrompt
