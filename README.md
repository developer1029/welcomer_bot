# Welcome Bot

This is a simple welcome bot for Discord that sends a welcome message to new members when they join the server.

## Features

- Customizable command prefix
- Customizable welcome message channel
- Customizable DM welcome message
- Help command with a list of available commands

## Requirements

- Python 3.8 or higher
- discord.py library (`pip install discord.py`)
- dotenv library (`pip install python-dotenv`)

## Usage

1. Clone this repository or download the code as a ZIP file.
2. Rename the `.env.example` file to `.env` and fill in your bot token and default command prefix.
3. Customize the welcome message channel and DM message settings if desired in the `custom_channels` and `custom_dm` dictionaries in the code.
4. Run the bot using the command `python bot.py`.

## Commands

- `setprefix [prefix]`: Set a custom command prefix for the server.
- `setchannel [channel]`: Set the channel where the welcome message will be sent.
- `setdm [on/off]`: Toggle whether the welcome message will be sent via DM to new members.
- `help`: Show a list of available commands.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
