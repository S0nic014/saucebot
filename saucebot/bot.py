import os
import sys
import pathlib
import tempfile
import ctypes
from discord.ext import commands
from dotenv import load_dotenv
from saucebot.logger import Logger


DISCORD_TOKKEN_VAR = 'DISCORD_TOKEN'
COGS_DIR = pathlib.Path.cwd() / 'cogs'
COMMAND_PREFIX = '?'
LOCK_FILE = pathlib.Path(tempfile.gettempdir()) / 'saucebot.lock'


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
            Logger.error('Discord token is missing. Add DISCORD_TOKEN=yourtoken to .env file. https://discord.com/developers/applications/')
            return

        bot.run(os.getenv(DISCORD_TOKKEN_VAR))
    except Exception:
        Logger.exception('Unhandled exception')


if __name__ == '__main__':
    try:
        if LOCK_FILE.is_file():
            os.unlink(LOCK_FILE.as_posix())
    except WindowsError:
        msg_box = ctypes.windll.user32.MessageBoxW
        msg_box(None, 'Bot instance is already running!', 'Saucebot', 0)
        sys.exit(0)

    with open(LOCK_FILE.as_posix(), 'wb') as lockfileobj:
        main()
    os.unlink(LOCK_FILE.as_posix())
