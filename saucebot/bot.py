import os
import pathlib
from discord.ext import commands
from dotenv import load_dotenv
from saucebot.logger import Logger


DISCORD_TOKKEN_VAR = 'DISCORD_TOKEN'
COGS_DIR = pathlib.Path.cwd() / 'cogs'
COMMAND_PREFIX = '?'


def list_cogs() -> list:
    cogs = []
    for cog_file in COGS_DIR.glob('*.py'):
        fname = cog_file.name.removesuffix('.py')
        cogs.append(f'cogs.{fname}')
    return cogs


def main():
    Logger.write_to_rotating_file('bot.log')
    try:
        bot = commands.Bot(COMMAND_PREFIX)
        # Load extensions
        for ext in list_cogs():
            bot.load_extension(ext)
            Logger.info(f'Loaded extension: {ext}')

        # Start
        load_dotenv()
        if not os.getenv(DISCORD_TOKKEN_VAR):
            Logger.warning('Discord token is missing. Add DISCORD_TOKEN=yourtoken to .env file. https://discord.com/developers/applications/')
            input('Press any key to close...')
            return

        bot.run(os.getenv(DISCORD_TOKKEN_VAR))
    except Exception:
        Logger.exception('Unhandled exception')
        input()


if __name__ == '__main__':
    main()
