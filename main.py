import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import os
import asyncio
from dotenv import load_dotenv

# Tải biến môi trường từ tệp .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)


class BasicStatement(commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')  
        print(f'Logged in as: {self.bot.user}')  
        print("______________________")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(os.getenv('CHANNEL_ID'))
        await channel.send(f'Hello {member.mention}! Welcome to the server.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(os.getenv('CHANNEL_ID'))
        await channel.send(f'Goodbye {member.mention}!')

    @commands.command()
    async def hello(self, ctx):
        print('Hello command received.')  
        await ctx.send('Lo cc')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send('You do not have permission to kick!')


async def main():
    # Add the PlayAudio cog to the bot
    await client.add_cog(BasicStatement(client))

    # Run the bot
    await client.start(os.getenv('DISCORD_TOKEN'))

# Start the bot
asyncio.run(main())

