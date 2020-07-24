# discord-eprompt

[![PyPI version](https://badge.fury.io/py/discord-eprompt.svg)](https://badge.fury.io/py/discord-eprompt)

Reaction-based user input prompts for Discord bots

## Testing

Due to the difficulty of unit-testing this stuff there is currently no automated testing suite. However, there is the
`example.py` script which will demonstrate the bot's funcitonality. You will need your own bot and your own server to
use this; see the [Discord dev portal](https://discord.com/developers) for more information.

To use it, copy the `example.json.template` file to `example.json`. Then, edit the new file and replace the value for 
`token` with your bot's token, and `guild` with the ID of the guild to which the tester should send messages. The bot
will use the first available text channel to send its messages.
