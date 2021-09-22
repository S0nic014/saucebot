import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands.context import Context
from saucenao_api import SauceNao
from saucebot.logger import Logger


class SauceCog(commands.Cog):

    NAO_KEY_VAR = 'NAO_KEY'

    def __init__(self, bot) -> None:
        super().__init__()
        load_dotenv()
        if not os.getenv(self.NAO_KEY_VAR):
            Logger.warning('SauceNao API key missing. Add NAO=yourkey to .env file. Get one from https://saucenao.com/user.php?page=search-api')

        self.nao = SauceNao(api_key=os.getenv(self.NAO_KEY_VAR))
        self.bot = bot

    async def get_sauce_from_message(self, msg: discord.Message):
        if not msg.attachments:
            await msg.reply('No attachements/ references found :c')
            return

        if 'video' in msg.attachments[0].content_type:
            await msg.reply('Can\'t search by video :c')
            return

        try:
            src_file = await msg.attachments[0].to_file()
            results = self.nao.from_file(src_file.fp)
            if not results:
                await msg.reply('No results found :c')
                return

            await msg.reply(f'Best simularity: {results[0].similarity}\nLink: {results[0].urls[-1]}')

        except Exception:
            Logger.exception('Sauce exception')
            await msg.reply('Error when finding sauce, slap the dev :c')

    @commands.command()
    async def sauce(self, ctx: Context, ref_url: str = None):
        msg: discord.Message = ctx.message
        if isinstance(ref_url, str) and ref_url:
            # Get referenced message
            if not ref_url.startswith('https://'):
                await msg.reply('Invalid message URL')
                return
            ref_url_parts = ref_url.split('/')
            sauce_msg: discord.Message = await self.bot.get_guild(int(ref_url_parts[-3])).get_channel(int(ref_url_parts[-2])).fetch_message(int(ref_url_parts[-1]))

            await self.get_sauce_from_message(sauce_msg)
            return

        elif ctx.message.attachments:
            await self.get_sauce_from_message(ctx.message)

        else:
            await ctx.message.reply('Attachment or message link required!')


def setup(bot):
    bot.add_cog(SauceCog(bot))
