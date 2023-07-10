import discord
import sqlite3
import asyncio
import os
import dotenv

from discord import app_commands, utils
from datetime import timedelta
from discord.ext import commands, tasks
from itertools import cycle

dotenv.load_dotenv()
discord_token = os.getenv('discord_token')

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="s!", intents=intents)
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
    print(f"Successfully logged in as {client.user}")


@client.tree.command(name='help', description="Displays information.")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="TheHive Information & Commands", color=0x00ff00)
    embed.add_field(name="/start", value=f"Select a game to play.", inline=False)
    embed.add_field(name="/level", value="Check your global level.", inline=False)
    embed.add_field(name="/leaderboard", value=f"Checkout the top 10 players.", inline=False)
    embed.add_field(name="/dev", value=f"Learn more about the developer", inline=False)

    # Send the embedded message to the channel where the command was invoked
    await interaction.response.send_message(embed=embed, ephemeral=False)


@client.tree.command(
    name="start",
    description="Select a game to play.",
)
@app_commands.describe(games="Pick a game to play!")
@app_commands.choices(games=[
    discord.app_commands.Choice(name="Tetris", value=1),
    discord.app_commands.Choice(name="Mines", value=2),
    discord.app_commands.Choice(name="Sudoku", value=3),
])
async def start_command(interaction: discord.Interaction, games: discord.app_commands.Choice[int]):
    game = games.value
    if game == 1:
        await play_tetris(interaction)
    #elif game == 2:
        #await play_mines(interaction)
    #elif game == 3:
        #await play_sudoku(interaction)
    else:
        await interaction.response.send_message("Invalid game selection.", ephemeral=True)


async def play_tetris(interaction: discord.Interaction):
    await interaction.response.defer()

    tetris_board = discord.Embed(title="TETRIS", description=":black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:\n:black_large_square::black_large_square::black_large_square::black_large_square::black_large_square:", color=0x5865F2)
    message = await interaction.followup.send(embed=tetris_board)

    # Add reactions to the message
    reactions = ['⬅️', '➡️', '⬇️', '⏸️']
    for reaction in reactions:
        await message.add_reaction(reaction)

    # TODO add logic to remove user reactions after every reaction & ignore bot reactions
    

"""
async def play_mines(interaction: discord.Interaction):
    # Mines game logic goes here
    # Example: Start a game of Mines and display the game board
    game_board = create_mines_board()
    game_over = False

    while not game_over:
        # Display the game board and wait for user input
        await display_mines_board(interaction, game_board)
        user_input = await wait_for_mines_input(interaction)

        # Process user input and update the game board
        # Example: Reveal a cell or mark it as a mine based on user input
        update_mines_board(game_board, user_input)

        # Check if the game is over (e.g., a mine was hit)
        game_over = is_mines_game_over(game_board)

    # Game over, display the final game board and score
    await display_mines_board(interaction, game_board)
    await interaction.response.send_message("Game over!", ephemeral=True)


async def play_sudoku(interaction: discord.Interaction):
    # Sudoku game logic goes here
    # Example: Start a game of Sudoku and display the puzzle
    puzzle = create_sudoku_puzzle()
    solved = False

    while not solved:
        # Display the puzzle and wait for user input
        await display_sudoku_puzzle(interaction, puzzle)
        user_input = await wait_for_sudoku_input(interaction)

        # Process user input and update the puzzle
        # Example: Fill in a cell or clear it based on user input
        update_sudoku_puzzle(puzzle, user_input)

        # Check if the puzzle is solved
        solved = is_sudoku_puzzle_solved(puzzle)

    # Puzzle solved, display the final puzzle
    await display_sudoku_puzzle(interaction, puzzle)
    await interaction.response.send_message("Puzzle solved!", ephemeral=True)
"""

async def main():
    async with client:
        await client.start(discord_token)

asyncio.run(main())
