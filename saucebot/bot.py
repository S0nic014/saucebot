import os
import pathlib
from discord.ext import commands
from dotenv import load_dotenv
from saucebot.logger import Logger


COGS_DIR = pathlib.Path.cwd() / 'saucebot' / 'cogs'
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
        for ext in list_cogs():
            bot.load_extension(ext)
            Logger.info(f'Loaded extension: {ext}')

        load_dotenv()
        bot.run(os.getenv('TOKEN'))
    except Exception:
        Logger.exception('Unhandled exception')


if __name__ == '__main__':
    main()
