import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Member
from discord import FFmpegPCMAudio
import requests
import json
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

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


class PlayAudio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Joined {channel}")
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, url):
        voice_client = ctx.guild.voice_client

        if not voice_client:
            await ctx.send("I need to be in a voice channel to play audio.")
            return

        try:
            ffmpeg_audio = discord.FFmpegPCMAudio(url)
            voice_client.play(ffmpeg_audio)
            await ctx.send(f"Now playing: {url}")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if not voice_client or not voice_client.is_playing():
            await ctx.send("There is no audio playing.")
            return

        voice_client.pause()
        await ctx.send("Paused the audio.")

    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if not voice_client or not voice_client.is_paused():
            await ctx.send("The audio is not paused.")
            return

        voice_client.resume()
        await ctx.send("Resumed the audio.")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if not voice_client or not voice_client.is_playing():
            await ctx.send("There is no audio playing.")
            return

        voice_client.stop()
        await ctx.send("Stopped the audio.")

    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel.")
        else:
            await ctx.send("I am not connected to a voice channel.")

async def main():
    # Add the PlayAudio cog to the bot
    await client.add_cog(PlayAudio(client))
    await client.add_cog(BasicStatement(client))

    # Run the bot
    await client.start(os.getenv('DISCORD_TOKEN'))

# Start the bot
asyncio.run(main())

