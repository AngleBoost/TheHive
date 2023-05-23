
# Programmed by BoostieDev#0001

import discord
import sqlite3
import datetime
import math
import asyncio
import requests
import aiohttp
import random
import json
import pytz
import os
import dotenv

# from io import BytesIO
from discord import app_commands, utils
from datetime import timedelta
from discord.ext import commands, tasks
from itertools import cycle
# from discord.ui import Button, View

dotenv.load_dotenv()
discord_token = os.getenv('discord_token')


user_settings = {}
message_counts = {}

intents = discord.Intents.all()
intents.members = True

client =commands.Bot(command_prefix="s!", intents=intents)
bot_status = cycle([
    "/help"
])
client.remove_command('help')


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    try: 
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except:
        print('already synced')

    change_status.start()
    print(f"Sucessfully logged in as {client.user}")

user_log_channel_id = 964660390984286258
mod_log_channel_id = 964656541384970280

anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
too_many_violations = commands.CooldownMapping.from_cooldown(3, 60, commands.BucketType.member)

muted_users = []
banned_users_two = []
locked_channels = []
conn = sqlite3.connect('databases/user_levels.db')
c = conn.cursor()
c.execute('''
        CREATE TABLE IF NOT EXISTS user_levels
        (user_id TEXT, xp INTEGER, level INTEGER)
        ''')
conn.commit()

@client.event
@commands.cooldown(1, 30, commands.BucketType.user) # 1 message per 30 seconds per user
async def on_message(message):

    if not message.author.bot:
        user_id = str(message.author.id)
        c.execute("SELECT xp, level FROM user_levels WHERE user_id=?", (user_id,))
        result = c.fetchone()
        if result is None:
            xp = 0
            level = 1
            c.execute("INSERT INTO user_levels (user_id, xp, level) VALUES (?, ?, ?)", (user_id, xp, level))
        else:
            xp, level = result
        xp += 13 # Increase XP by 13 for each message
        if xp >= level * 100: # If the user has earned enough XP to level up
            xp -= level * 100 # Subtract current level's XP requirement from total XP
            level += 1


        if level >= 5:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 10:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 20:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)    
        elif level >= 40:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 60:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 75: # Assign role perks if user reaches level 75
            role = message.guild.get_role(role_id) # Replace role_id with the actual ID of the role you want to assign
            await message.author.add_roles(role)
        elif level >= 90:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 100:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 120:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 150:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 200:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)
        elif level >= 300:
            role = message.guild.get_role(role_id)
            await message.author.add_roles(role)

        c.execute("UPDATE user_levels SET xp=?, level=? WHERE user_id=?", (xp, level, user_id))
        conn.commit()
    await client.process_commands(message)

    hate_speech = []
    if message.content.lower() in hate_speech:
        await message.delete()
        author = message.author
        if author.id not in muted_users:
            muted_users.append(author.id)
            await message.author.timeout(timedelta(minutes = 5), reason = "Hate Speech Detected")
            try:
                embed = discord.Embed(title="Warning", description=f"{message.author.mention}, you have been timed out for saying a banned word!")
                await message.author.send(embed=embed)
            except: 
                await message.channel.send(f"{message.author.mention}, you have been timed out for saying a banned word!", delete_after = 2)

    ban_list = []
    if message.content.lower() in ban_list:
        await message.delete()
        author = message.author
        if author.id not in banned_users_two:
            banned_users_two.append(author.id)
            await message.author.ban(reason = "Banned Slur Detected")

    if message.channel.id in locked_channels:
        await message.delete()
    elif type(message.channel) is not discord.TextChannel or message.author.bot: return
    bucket = anti_spam.get_bucket(message)
    retry_after = bucket.update_rate_limit()
    if retry_after:
        await message.delete()
        embed = discord.Embed(title="Warning", description=f"{message.author.mention}, you have been warned for spamming. Please slow down on your messaging!")
        await message.channel.send(embed=embed, delete_after = 2)
        violations = too_many_violations.get_bucket(message)
        check = violations.update_rate_limit()
        if check:
            await message.author.timeout(timedelta(minutes = 10), reason = "Spamming")
            try:
                embed = discord.Embed(title="Warning", description=f"{message.author.mention}, you have been timed out for spamming!")
                await message.author.send(embed=embed)
            except: 
                await message.channel.send(f"{message.author.mention}, you have been timed out for spamming!", delete_after = 2)

    # Get the list of blocked links
    banned_links=[
       "www.example.com"
        ]

    timeout_links=[
        "www.example.net"
        ]
    
    # Check if the message contains any of the blocked links.
    for link in banned_links:
        if link in message.content:
            # If the message contains a blocked link, delete it.
            await message.delete()
            await message.author.ban(reason = "Bad Link Detected")
            
    for link in timeout_links:
        if link in message.content:
            # If the message contains a blocked link, delete it.
            await message.delete()
            await timeout(timedelta(minutes = 5), reason = "Bad Link Detected")

    
    nsfw_words = []

    if message.content.lower() in nsfw_words:
        await message.author.timeout(timedelta(minutes = 5), reason = "NSFW word Detected")
        try:
            embed = discord.Embed(title="Warning", description=f"{message.author.mention}, you have been timed out for saying a nsfw word!")
            await message.author.send(embed=embed)
        except: 
            await message.channel.send(f"{message.author.mention}, you have been timed out for saying a nsfw word!", delete_after = 2)


@client.event
async def on_message_edit(before, after):
    if after.author.bot:
        return

    log_channel = client.get_channel(user_log_channel_id)

    embed = discord.Embed(
        title='Message Edited',
        description=f'A message by {after.author.mention} was edited in {after.channel.mention}.',
        color=discord.Color.orange()
    )
    embed.add_field(name='Before', value=before.content, inline=False)
    embed.add_field(name='After', value=after.content, inline=False)
    embed.set_footer(text=f'Message ID: {after.id}')

    await log_channel.send(embed=embed)


@client.event
async def on_message_delete(message):
    log_channel = client.get_channel(user_log_channel_id)
    mod_role = discord.utils.get(message.guild.roles, name='Moderator')

    if mod_role in message.author.roles:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.url.endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4")):
                embed = discord.Embed(
                    title='Image/Video Deleted',
                    description=f'An image/video was deleted from {message.channel.mention}.',
                    color=discord.Color.red()
                )
                embed.set_image(url=attachment.url)
                embed.set_footer(text=f'Message ID: {message.id}')
                await log_channel.send(embed=embed)

    if not message.content:
        return

    embed = discord.Embed(
        title='Message Deleted',
        description=f'A message by {message.author.mention} was deleted from {message.channel.mention}.',
        color=discord.Color.red()
    )
    embed.add_field(name='Message Content', value=message.content, inline=False)
    embed.set_footer(text=f'Message ID: {message.id}')
    await log_channel.send(embed=embed)

@client.event
async def on_member_ban(guild, user):
    log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(
        title='User Banned',
        description=f'{user} was banned from the server.',
        color=discord.Color.red()
    )
    embed.set_footer(text=f'User ID: {user.id}')
    print(f"{user} was banned from the server.")
    await log_channel.send(embed=embed)

@client.event
async def on_member_unban(guild, user):
    log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(
        title='User Unbanned',
        description=f'{user} was unbanned from the server.',
        color=discord.Color.green()
    )
    embed.set_footer(text=f'User ID: {user.id}')
    print(f"{user} was unbanned from the server.")
    await log_channel.send(embed=embed)

@client.event
async def on_member_join(member):
    log_channel = client.get_channel(user_log_channel_id)
    server = member.guild
    embed = discord.Embed(
        title='Member Joined',
        description=f'{member} joined the server.',
        color=discord.Color.green()
    )
    embed.set_footer(text=f'User ID: {member.id} | Members: {server.member_count}')
    print(f"{member} joined the server.")
    await log_channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    log_channel = client.get_channel(user_log_channel_id)
    server = member.guild
    embed = discord.Embed(
        title='Member Left',
        description=f'{member} left the server.',
        color=discord.Color.red()
    )
    embed.set_footer(text=f'User ID: {member.id} | Members: {server.member_count}')
    print(f"{member} left the server.")
    await log_channel.send(embed=embed)


@client.event
async def on_member_update(before, after):
    log_channel = client.get_channel(user_log_channel_id)
    
    # Check for nickname change
    if before.nick != after.nick:
        embed = discord.Embed(
            title='Nickname Changed',
            description=f'{before.mention} changed their nickname to {after.nick}.',
            color=discord.Color.orange()
        )
        embed.set_footer(text=f'User ID: {after.id} | Username: {before}')
        await log_channel.send(embed=embed)

        # Check if new nickname contains any bad words
        bad_words = []
        for word in bad_words:
            if word in after.display_name:
                new_name = "<ChangeName>"
                await after.edit(nick=new_name)
                embed = discord.Embed(
                    title='Nickname Changed',
                    description=f'{after} had their nickname automatically changed to {new_name} due to inappropriate language.',
                    color=discord.Color.red()
                )
                embed.set_footer(text=f'User ID: {after.id}')
                await log_channel.send(embed=embed)
                break


@client.event
async def on_guild_channel_delete(channel):
    log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(
        title='Channel Deleted',
        description=f'{channel} was deleted.',
        color=discord.Color.red()
    )
    embed.set_footer(text=f'Channel ID: {channel.id}')
    await log_channel.send(embed=embed)

@client.tree.command(name='status', description="Gives the status on the bot.")
async def status(interaction: discord.Interaction):
    # Get bot's ping
    bot_ping = round(client.latency * 1000)


    # Get the current time in CDT
    tz = pytz.timezone('America/Chicago')
    current_time = datetime.datetime.now(tz)
    current_time_str = current_time.strftime("%I:%M%p")
    current_date_str = current_time.strftime("%Y-%m-%d")
    

    # Create the embedded message
    embed = discord.Embed(title="Bot Status", color=0x00ff00)
    embed.add_field(name="Bot Ping", value=f"🏓 {bot_ping}ms", inline=False)
    embed.add_field(name="Bot Time Zone", value="CST", inline=False)
    embed.add_field(name="Bot Current Time", value=f"🕒 {current_time_str}", inline=False)
    embed.add_field(name="Bot Current Date", value=f"📅 {current_date_str}", inline=False)

    # Send the embedded message to the channel where the command was invoked
    await interaction.response.send_message(embed=embed, ephemeral=False)


@client.tree.command(name='level', description="Displays the member's level")
async def level(interaction: discord.Interaction, member: discord.Member):
    user_id = str(member.id)
    c.execute("SELECT xp, level FROM user_levels WHERE user_id=?", (user_id,))
    result = c.fetchone()
    if result is None:
        xp = 0
        level = 1
    else:
        xp, level = result

    # Create an embed with the user's level information and progress bar
    progress_percentage = math.ceil((xp / (level * 100)) * 100)
    progress_bar = ''.join(['█' for i in range(progress_percentage // 5)])
    progress_bar += ''.join(['░' for i in range(20 - progress_percentage // 5)])
    progress = f"{progress_percentage}% ({xp}/{level*100} XP) {progress_bar}"

    embed = discord.Embed(title=f"{member.display_name}'s Level", color=0xFD7720)
    embed.add_field(name="XP", value=progress, inline=False)
    embed.add_field(name="Level", value=f"{level}")
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='leaderboard', description="Shows a leaderboard") # help slash command
async def leaderboard(interaction: discord.Interaction):
    c.execute("SELECT user_id, xp, level FROM user_levels ORDER BY level DESC, xp DESC LIMIT 5")
    result = c.fetchall()
    # Create a leaderboard embed
    embed = discord.Embed(title="Leaderboard", color=0xFD7720)
    for i, row in enumerate(result):
        user_id, xp, level = row
        member = await client.fetch_user(int(user_id))
        embed.add_field(name=f"{i+1}. {member.display_name}", value=f"XP: {xp} | Level: {level}", inline=False)
    await interaction.response.send_message(embed=embed)


locked_channels = []

@client.tree.command(name="lock", description="locks a mention channel")
@app_commands.checks.has_permissions(ban_members=True)
async def lock(interaction: discord.Interaction, channel: discord.TextChannel = None):
    if not channel:
        channel = interaction.channel

    if channel.id in locked_channels:
        await interaction.response.send_message("This channel is already locked.")
    else:
        await interaction.response.send_message("This channel is now locked.")
        locked_channels.append(channel.id)

@client.tree.command(name="unlock", description="unlocks a mention channel")
@app_commands.checks.has_permissions(ban_members=True)
async def unlock(interaction: discord.Interaction, channel: discord.TextChannel = None):
    if not channel:
        channel = interaction.channel

    if channel.id in locked_channels:
        locked_channels.remove(channel.id)
        await interaction.response.send_message("This channel is now unlocked.")
    else:
        await interaction.response.send_message("This channel was not locked.")


@client.tree.command(name='timeout', description='Times out a member.')
@app_commands.checks.has_permissions(kick_members=True)
async def timeout(interaction: discord.Interaction, member: discord.User, *, reason: str, minutes: int):
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    mod = interaction.user
    print(f"{mod} timed out {member}.")
    embed = discord.Embed(title='Timeout Successful', description=f'{member.mention} has been timed out for {minutes} minute(s).', color=0xFD7720)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name='unban', description='Unbans a user.')
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, userid: discord.User):
    guild = interaction.guild
    mod = interaction.user
    await guild.unban(user=userid)
    print(f"{mod} unbanned {userid}.")
    embed = discord.Embed(title='Unban Successful', description=f'{userid.mention} has been unbanned.', color=0xFD7720)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='softban', description='Bans and immediately unbans a user.')
@app_commands.checks.has_permissions(ban_members=True)
async def softban(interaction: discord.Interaction, userid: discord.User, *, reason: str):
    guild = interaction.guild
    mod = interaction.user
    await userid.ban(reason=reason)
    await guild.unban(user=userid)
    print(f"{mod} softbanned {userid}.")
    embed = discord.Embed(title='Softban Successful', description=f'{userid.mention} has been softbanned for {reason}.', color=0xFD7720)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='ban', description='Bans a user.')
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.User, *, reason: str):
    mod = interaction.user
    await member.ban(reason=f'{reason} - by {mod}')
    print(f"{mod} banned {member}.")
    embed = discord.Embed(title='Ban Successful', description=f'{member.mention} has been banned by {mod.mention} for {reason}.', color=0xFD7720)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='kick', description='Kicks a user.')
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.User, *, reason: str):
    mod = interaction.user
    await member.kick(reason=reason)
    embed = discord.Embed(title='Kick Successful', description=f'{member.mention} has been kicked by {mod.mention} for {reason}.', color=0xFD7720)
    print(f"{mod} kicked {member}.")
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='clear', description='Clears messages.')
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    mod = interaction.user
    await interaction.channel.purge(limit=amount)
    print(f"{mod} cleared {amount} messages.")
    embed = discord.Embed(title='Clear Successful', description=f'{amount} message(s) have been cleared.', color=0xFD7720)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name='nuke', description='Nukes a selected channel')
@app_commands.checks.has_permissions(manage_channels=True)
async def nuke(interaction: discord.Interaction, channel: discord.TextChannel):
    mod = interaction.user
    await interaction.response.defer()

    confirm_msg = await interaction.followup.send(content=f"Are you sure you want to nuke {channel.mention}?", ephemeral=True)
    await confirm_msg.add_reaction('✅')
    await confirm_msg.add_reaction('❌')

    def check(reaction, user):
        return user == interaction.user and str(reaction.emoji) in ['✅', '❌']

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await confirm_msg.edit(content='', embed=discord.Embed(title='Confirmation canceled.',color=discord.Color.red()))
        return
    if str(reaction.emoji) == '❌':
        await confirm_msg.edit(content='', embed=discord.Embed(title='Confirmation canceled.',color=discord.Color.red()))
        return

    await confirm_msg.edit(embed=discord.Embed(
        title='Nuking...',
        description=f'{channel.mention} is being nuked in 5 seconds!',
        color=discord.Color.red()
    ))

    message = await channel.send("THIS CHANNEL IS BEING NUKED IN 5")
    print(f"{mod} nuked {channel.name} messages.")
    for i in range(4, -1, -1):
        await asyncio.sleep(1)
        await message.edit(content=f'THIS CHANNEL IS BEING NUKED IN {i}')

    new_channel = await channel.clone(reason="Has been nuked!")
    await channel.delete()

    await new_channel.send("Nuked the channel successfully! :boom:")


@client.tree.command(name="server", description="Displays server infomation.")
@app_commands.checks.has_permissions(kick_members=True)
async def server(interaction: discord.Interaction):
    embed = discord.Embed(title=f"{interaction.guild.name} Info",description="Information of this Server", color=0xFD7720)
    embed.add_field(name='🆔Server ID', value=f"{interaction.guild.id}", inline=False)
    embed.add_field(name='📆Created on',value=interaction.guild.created_at.strftime("%b %d %Y"),inline=False)
    embed.add_field(name='👑Owner',value=f"{interaction.guild.owner.mention}",inline=False)
    embed.add_field(name='👥Members',value=f'{interaction.guild.member_count} Members',inline=False)
    embed.add_field(name='💬Channels',value=f'{len(interaction.guild.text_channels)} Text | {len(interaction.guild.voice_channels)} Voice',inline=False)
    embed.set_thumbnail(url=interaction.guild.icon.url)
    await interaction.response.send_message(embed=embed, ephemeral=False)


@client.tree.command(name='warn', description="Issues a warning to the specified user.")
@app_commands.checks.has_permissions(kick_members=True)
async def warn(interaction: discord.Interaction, member: discord.User, *, reason: str):
        mod = interaction.user

        conn = sqlite3.connect('databases/warnings.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
            user_id INTEGER,
            warning_number INTEGER,
            reason TEXT,
            PRIMARY KEY (user_id, warning_number)
            )
            ''')

        cursor.execute(f'SELECT COUNT(*) FROM warnings WHERE user_id={member.id}')
        result = cursor.fetchone()[0]
        warnings = result + 1

        cursor.execute(f'INSERT INTO warnings(user_id, warning_number, reason) VALUES({member.id}, {warnings}, "{reason}")')
        conn.commit()
        conn.close()

        print(f"{mod} warned {member}.")

        if warnings == 1:
            embed = discord.Embed(title="Warning", description=f"{member.mention} has been warned. They now have 1 warning.", color=0xFD7720)
            embed.set_thumbnail(url="")
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Punishment", value=f"Verbal Warning")
            await interaction.response.send_message(embed=embed)

        elif warnings == 2:
            embed = discord.Embed(title="Warning", description=f"{member.mention} has been warned. They now have 2 warnings.", color=0xFD7720)
            embed.set_thumbnail(url="")
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Punishment", value=f"{member.mention} has been timeout for 5 minutes.")
            await interaction.response.send_message(embed=embed)
            await member.timeout(timedelta(minutes = 5), reason = reason)

        elif warnings == 3:
            embed = discord.Embed(title="Warning", description=f"{member.mention} has been warned. They now have 3 warnings.", color=0xFD7720)
            embed.set_thumbnail(url="")
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Punishment", value=f"{member.mention} has been timeout for 10 minutes.")
            await interaction.response.send_message(embed=embed)
            await member.timeout(timedelta(minutes = 10), reason = reason)

        elif warnings == 4:
            await interaction.guild.kick(member)
            embed = discord.Embed(title="Warning", description=f"{member.mention} has been warned. They now have 4 warnings.", color=0xFD7720)
            embed.set_thumbnail(url="")
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Punishment", value=f"{member.mention} has been kicked.")
            await interaction.response.send_message(embed=embed)

        elif warnings >= 5:
            await interaction.guild.ban(member)
            embed = discord.Embed(title="Warning", description=f"{member.mention} has been warned. They now have 5 warnings.", color=0xFD7720)
            embed.set_thumbnail(url="")
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Punishment", value=f"{member.mention} has been banned.")
            await interaction.response.send_message(embed=embed)


@client.tree.command(name='delwarn', description="Deletes a warning for the specified user.")
@app_commands.checks.has_permissions(ban_members=True)
async def delwarn(interaction: discord.Interaction, member: discord.User, number: int):
    mod = interaction.user
    try:
        conn = sqlite3.connect('databases/warnings.db')
        cursor = conn.cursor()
        
        # Delete the first warning for the specified user
        cursor.execute(f"DELETE FROM warnings WHERE user_id='{member.id}' AND warning_number={number}")
        
        # Get the new warning count for the user
        cursor.execute(f"SELECT COUNT(*) FROM warnings WHERE user_id='{member.id}'")
        result = cursor.fetchone()
        warnings = result[0]
        print(f"{mod} deleted a warning from {member}.")
        
        if warnings > 0:
            embed = discord.Embed(
                title="Deleting Warning...",
                description=f"Removed 1 warning from {member.mention}. They now have {warnings} warning(s).",
                color=0xFD7720
            )
        else:
            embed = discord.Embed(
                title="Deleting Warning...",
                description=f"All warnings for {member.mention} have been removed.",
                color=0xFD7720
            )
        
        conn.commit()
        
        await interaction.response.send_message(embed=embed)

    except sqlite3.Error as e:
        await interaction.response.send_message(f'An error occurred while accessing the database: {e}')
        
    finally:
        conn.close()


@client.tree.command(name='cwarn', description='Clears all warns from user')
@app_commands.checks.has_permissions(ban_members=True)
async def cwarn(interaction: discord.Interaction, member: discord.User):
    mod = interaction.user
    conn = sqlite3.connect('databases/warnings.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM warnings WHERE user_id='{member.id}'")
        conn.commit()
        print(f"{mod} cleared all warnings from {member}.")
        
        embed = discord.Embed(
            title="Clearing Warnings...",
            description=f"Cleared all warnings from {member.mention}.",
            color=0xFD7720
        )
        await interaction.response.send_message(embed=embed)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        await interaction.response.send_message(f'An error occurred while accessing the database: {e}', delete_after=3)
        
    finally:
        cursor.close()
        conn.close()


@client.tree.command(name='warnings', description="Displays the number of warnings a user has received.")
@app_commands.checks.has_permissions(kick_members=True)
async def warnings(interaction: discord.Interaction, member: discord.User):
        try:
            conn = sqlite3.connect('databases/warnings.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM warnings WHERE user_id={member.id}')
            results = cursor.fetchall()

            if results:
                reasons = ""
                for result in results:
                    warning_number = result[1]
                    reason = result[2]
                    reasons += f"{warning_number} warn: {reason}\n"

                embed = discord.Embed(title="Warning List", description=f"{member.mention} has {len(results)} warning(s).", color=0xFD7720)
                embed.add_field(name="Reasons", value=reasons)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f'{member.mention} has no warnings.')

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            await interaction.response.send_message(f'An error occurred while accessing the database: {e}')

        finally:
            conn.close()

@client.tree.command(name='remind-me', description="Set a reminder")
async def remindme(interaction: discord.Interaction, time_str: str, *, reminder_message: str):
    await interaction.response.defer()
    # Parse the time string
    try:
        time_amount, time_unit = time_str[:-1], time_str[-1]
        time_amount = int(time_amount)
        if time_unit == 's':
            delta = datetime.timedelta(seconds=time_amount)
        elif time_unit == 'm':
            delta = datetime.timedelta(minutes=time_amount)
        elif time_unit == 'h':
            delta = datetime.timedelta(hours=time_amount)
        elif time_unit == 'd':
            delta = datetime.timedelta(days=time_amount)
        else:
            await interaction.followup.send('Invalid time unit! Please use s, m, h, or d. Example: /remindme 1h Go for a walk.')
            return
    except ValueError:
        await interaction.followup.send('Invalid time format! Please use a number followed by s, m, h, or d. Example: /remindme 1h Go for a walk.')
        return

    # Set the reminder
    await interaction.followup.send('Your reminder has been set. I will send you a DM when it is time so please have your DMs open to me.')
    await asyncio.sleep(delta.total_seconds())
    await interaction.user.send(f'Reminder: {reminder_message}')


@client.tree.command(name="help", description="Get help for commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Commands", description="List of available slash commands", color=0xFD7720)
    embed.add_field(name="Moderation", value="kick, ban, softban, warn, delwarn, cwarn, lock, unlock, unban, timeout, nuke, clear, whois, server, warnings", inline=False)
    embed.add_field(name="Fun", value="8ball, roll, rps, catfact, funnyrate, ship, joke", inline=False)
    embed.add_field(name="Leveling", value="level, leaderboard", inline=False)
    embed.add_field(name="Reminders", value="remind-me", inline=False)
    embed.add_field(name="Social", value="socials, stream, followage", inline=False)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name='8ball', description='Let the 8 Ball Predict!')
async def _8ball(interaction: discord.Interaction, *, question: str):
        responses = [
            'As I see it, yes.',
            'Yes.',
            'Positive',
            'From my point of view, yes',
            'Convinced.',
            'Most Likley.',
            'Chances High',
            'No.',
            'Negative.',
            'Not Convinced.',
            'Perhaps.',
            'Not Sure',
            'Maybe',
            'I cannot predict now.',
            'Im to lazy to predict.',
            'I am tired. *proceeds with sleeping*'
            ]
        response = random.choice(responses)
        embed=discord.Embed(title="The Magic 8 Ball has Spoken!", color=0xFD7720)
        embed.add_field(name='Question: ', value=question, inline=True)
        embed.add_field(name='Answer: ', value=response, inline=False)
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='funnyrate', description='Let The Hive Rate your funny')
async def funnyrate(interaction: discord.Interaction):
        embed=discord.Embed(title=f"You are {random.randrange(101)}% funny!", color=0xFD7720)
        await interaction.response.send_message(embed=embed)


@client.tree.command(name='ship', description='unrelated to boats btw')
async def ship(interaction: discord.Interaction, member1: discord.User, member2: discord.User):
        """Ship two members together"""
        ship_percent = random.randint(1, 100)
        name1 = member1.name[:len(member1.name)//2]
        name2 = member2.name[len(member2.name)//2:]
        nameship = name1 + name2

        embed = discord.Embed(
            title=f"{member1.name} x {member2.name} = {nameship}",
            description=f"**Compatibility: {ship_percent}%**",
            color=0xFD7720
        )
    
        if ship_percent <= 35:
            embed.add_field(name="Result", value="😅 There doesn't seem to be such great chemistry going on, but who knows...?")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1067596766356185131/1068988991145259018/brokenheart_ship.gif")
        elif ship_percent > 35 and ship_percent <= 65:
            embed.add_field(name="Result", value="🫤 This combination has potential, how about a romantic dinner?")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1067596766356185131/1068989461083455548/thinking_ship.gif")
        elif ship_percent > 65:
            embed.add_field(name="Result", value="😍 Perfect combination! When will the wedding be?")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1067596766356185131/1068986257826402304/ship.gif")

        await interaction.response.send_message(embed=embed)


@client.tree.command(name='joke', description='Ask The Hive For A Funny')
async def joke(interaction: discord.Interaction):
        url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Dark,Pun,Spooky?blacklistFlags=nsfw,racist,sexist,explicit"
        try:
            res = requests.get(url)
            data = json.loads(res.text)
            if "setup" in data:
                joke = f"{data['setup']}...{data['delivery']}"
            else:
                joke = data["joke"]
            embed = discord.Embed(title="Joke", description=joke, color=0xFD7720)
            await interaction.response.send_message(embed=embed)
        except requests.exceptions.RequestException as e:
            await print(f"Error: {e}")


@client.tree.command(name='roll', description='Roll a dice')
async def roll(interaction: discord.Interaction):
        """Roll a dice"""
        roll = random.randint(1, 6)
        embed = discord.Embed(title=f"Rolling a dice...", description=f"You rolled a {roll}!", color=0xFD7720)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1067596766356185131/1068993152784023705/roll-the-dice.gif")
        await interaction.response.send_message(embed=embed) 

@client.tree.command(name='rps', description='Rock, Paper, Scissors')
async def rps(interaction: discord.Interaction, choice: str):
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)
        result = ""
        if choice.lower() not in choices:
            result = "Invalid choice. Please choose rock, paper or scissors."
        elif choice.lower() == computer_choice:
            result = "It's a tie! You both chose " + choice + "."
        elif (choice.lower() == "rock" and computer_choice == "scissors") or (choice.lower() == "paper" and computer_choice == "rock") or (choice.lower() == "scissors" and computer_choice == "paper"):
            result = "You win! " + choice + " beats " + computer_choice + "."
        else:
            result = "You lose! " + computer_choice + " beats " + choice + "."
        embed = discord.Embed(title="Rock, Paper, Scissors", description=result, color=0xFD7720)
        embed.set_footer(text="Powered by RPSAPI")
        await interaction.response.send_message(embed=embed)

@client.tree.command(name='catfact', description='Tells you a random cat fact')
async def catfact(interaction: discord.Interaction):
    url = "https://cat-fact.herokuapp.com/facts/random"
    fact = json.loads(requests.get(url).text)["text"]
    embed = discord.Embed(title="Fun Cat Fact", description=fact, color=0xFD7720)
    embed.set_footer(text="Powered by CatFactsAPI")
    await interaction.response.send_message(embed=embed)



@client.tree.command(name='socials', description="Follow example's socials")
async def socials(interaction: discord.Interaction):
    twitter_link = ""
    youtube_link = ""
    twitch_link = ""
    reddit_link = ""
    tiktok_link = ""
    instagram_link = "n"


    socials_embed = discord.Embed(title="Socials", description="Follow example's on their socials", color=0xFD7720)
    socials_embed.add_field(name="Twitter", value=f"[Follow]({twitter_link})")
    socials_embed.add_field(name="YouTube", value=f"[Subscribe]({youtube_link})")
    socials_embed.add_field(name="Twitch", value=f"[Watch]({twitch_link})")
    socials_embed.add_field(name="Riddit", value=f"[Follow]({reddit_link})")
    socials_embed.add_field(name="TikTok", value=f"[Follow]({tiktok_link})")
    socials_embed.add_field(name="Instagram", value=f"[Follow]({instagram_link})")
    socials_embed.set_thumbnail(url="") # TODO add thumbnail

    await interaction.response.send_message(embed=socials_embed)


async def main():
    async with client:
        await client.start(discord_token)

asyncio.run(main())

# Ctrl+Alt+F to stop following