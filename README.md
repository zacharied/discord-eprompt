# discord-eprompt

[![PyPI version](https://badge.fury.io/py/discord-eprompt.svg)](https://badge.fury.io/py/discord-eprompt)

Reaction-based user input prompts for Discord bots

## Usage

A *reaction prompt* is simply a message with a set of predefined reactions and a target user. The bot reacts to the 
message with its set of reactions, leaving what are basically buttons which can be clicked by users. Normally, clicking 
on a reaction would just increase the count of that reaction on the message.  With reaction prompts, however, a 
callback with the choice is fired as soon as the target user clicks on one, allowing bots to actively respond to the 
user's button selection.

The library maintains a number of constraints on the message before the target user makes a decision. Reactions by 
those other than the target user are removed immediately, as are reactions *by* the target user that aren't apart of 
the predefined list of choices.

This package provides one method, `react_prompt_response` which takes a Discord message and turns it into a reaction
prompt. See its own documentation for usage details.

## Testing

Due to the difficulty of unit-testing this stuff there is currently no automated testing suite. However, there is the
`example.py` script which will demonstrate the bot's funcitonality. You will need your own bot and your own server to
use this; see the [Discord dev portal](https://discord.com/developers) for more information.

To use it, copy the `example.json.template` file to `example.json`. Then, edit the new file and replace the value for 
`token` with your bot's token, and `guild` with the ID of the guild to which the tester should send messages. The bot
will use the first available text channel to send its messages.
