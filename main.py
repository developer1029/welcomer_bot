import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import subprocess

subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])


load_dotenv()

intents = discord.Intents.all()

default_prefix = os.getenv("DEFAULT_PREFIX", "!")
custom_prefixes = {}
custom_channels = {}
custom_dm = {}

bot = commands.Bot(command_prefix = lambda bot, message: get_prefix(bot, message), intents=intents, help_command=None)

@bot.event
async def on_ready():
    try:
        print(f'{bot.user.name} has connected to Discord!')
        activity = discord.Activity(type=discord.ActivityType.listening, name='?help')
        await bot.change_presence(activity=activity)
    except Exception as e:
        print(f'Error in on_ready(): {e}')


def get_prefix(bot, message):
    if message.guild.id in custom_prefixes:
        return custom_prefixes[message.guild.id]
    else:
        return default_prefix

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    custom_prefixes[ctx.guild.id] = prefix
    embed = discord.Embed(description=f"✅ The command prefix for this server has been set to **`{prefix}`**.", color=0xFF6C00)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setchannel(ctx, channel: discord.TextChannel):
    custom_channels[ctx.guild.id] = channel.id
    embed = discord.Embed(description=f"✅ **Success!** The welcome message will now be sent to the {channel.mention} channel.", color=0xFF6C00)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setdm(ctx, value: str):
    if isinstance(value, str):
        if value.lower() == 'on':
            custom_dm[ctx.guild.id] = True
            embed = discord.Embed(title="🟢 DM message enabled", description="The welcome message will now be sent via DM to new members.", color=0xFF6C00)
        elif value.lower() == 'off':
            custom_dm[ctx.guild.id] = False
            embed = discord.Embed(title="🔴 DM message disabled", description="The welcome message will no longer be sent via DM to new members.", color=0xFF6C00)
        else:
            embed = discord.Embed(description=":warning: You must specify either `on` or `off` to enable or disable DMs.", color=0xFF6C00)
    else:
        embed = discord.Embed(description=":warning: Invalid parameter type. Please enter a string value.", color=0xFF6C00)
    await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
    embed = discord.Embed(title=f":tada: Welcome to {member.guild.name}!", description=f"{member.mention}, thank you for joining our server! :tada:", color=0xFF6C00)
    embed.set_thumbnail(url=member.avatar.url)
    channel_id = custom_channels.get(member.guild.id)
    channel = discord.utils.get(member.guild.channels, id=channel_id) if channel_id else discord.utils.get(member.guild.channels, name='welcome')
    if channel is not None:
        await channel.send(embed=embed)
    if custom_dm.get(member.guild.id, True):
        await member.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title=":notebook_with_decorative_cover: Welcome Bot Commands", color=0xFF6C00)
    embed.add_field(name="setprefix", value="Set a custom command prefix for this server.", inline=False)
    embed.add_field(name="setchannel", value="Set the channel where the welcome message will be sent.", inline=False)
    embed.add_field(name="setdm", value="Toggle whether the welcome message will be sent via DM to new members.", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        error_message = ":x: You do not have permission to use this command."
    elif isinstance(error, commands.MissingRequiredArgument):
        error_message = f":warning: You must specify a {error.param.name}."
    elif isinstance(error, commands.CommandNotFound):
        error_message = ":x: Invalid command. Use `help` command to see a list of available commands."
    elif isinstance(error, commands.MemberNotFound):
        error_message = ":x: The specified member was not found."
    elif isinstance(error, commands.ChannelNotFound):
        error_message = ":x: The specified channel was not found."
    else:
        error_message = ":warning: An error occurred while processing the command."
        print(error)

    embed = discord.Embed(description=error_message, color=0xFF6C00)
    await ctx.send(embed=embed)


bot.run(os.getenv("BOT_TOKEN"))