import os
import discord
from discord.ext import commands, tasks
from multiprocessing import Pool, cpu_count
import asyncio

# Function to count folders in batch
def count_folders_in_batch(directory, subdirs):
    return sum(os.path.isdir(os.path.join(directory, subdir)) for subdir in subdirs)

# Function to count folders
def count_folders(directory):
    print(f"Checking directory: {directory}")
    subdirs = [subdir for subdir in os.listdir(directory) if not subdir.startswith('.') and os.path.isdir(os.path.join(directory, subdir))]
    with Pool(processes=cpu_count()) as pool:
        counts = pool.starmap(count_folders_in_batch, [(directory, subdirs[i:i+cpu_count()]) for i in range(0, len(subdirs), cpu_count())])
    return sum(counts)

# Discord bot token
TOKEN = 'YOUR_TOKEN'

# Intents
intents = discord.Intents.all()

# Prefix for bot commands
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store channel IDs
channel_ids = {}

# Function to get count for a folder
def get_count(directory):
    count = count_folders(directory)
    return count

# List of folders to track
folders = {
    "Movies": "/path/to/Movies",
    "Movies2": "/path/to/Movies",
    "Series": "/path/to/Series",
    "Series2": "/path/to/Series",
    # Add other folders with their paths here
}

# Function to update folder counts
async def update_folder_counts():
    await bot.wait_until_ready()
    while not bot.is_closed():
        guild = bot.guilds[0]  # Assuming the bot is in only one guild
        category_name = "Jellycine-Server-Stats"

        # Check if the category already exists
        category = discord.utils.get(guild.categories, name=category_name)
        await category.set_permissions(guild.default_role, view_channel=True)

        if category is None:
            # Category doesn't exist, create it
            category = await guild.create_category(category_name)
            await category.set_permissions(guild.default_role, view_channel=True)
            print(f"Created category: {category_name}")
        else:
            print(f"Category {category_name} already exists")

        # Delete all existing sub-channels under the category
        for channel in category.channels:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")

        # Combine movie counts from all movie directories
        all_movies_count = 0
        for movie_folder in ["Movies", "Movies2"]:
            movie_path = folders.get(movie_folder)
            if movie_path:
                all_movies_count += count_folders(movie_path)

        # Create "All Movies" channel and update count
        all_movies = discord.utils.get(category.channels, name="Total Movies")
        if all_movies is None:
            all_movies = await category.create_voice_channel("Total Movies")
            await all_movies.set_permissions(guild.default_role, view_channel=True)
            print("Created Total Movies channel")
        await all_movies.edit(name=f"Total Movies: {all_movies_count}")
        print(f"Updated Total Movies count: {all_movies_count}")

        # Create "ALLShows" channel and update count
        all_shows = discord.utils.get(category.channels, name="Total Shows")
        if all_shows is None:
            all_shows = await category.create_voice_channel("Total Shows")
            await all_shows.set_permissions(guild.default_role, view_channel=True)
            print("Created Total Shows channel")
        await all_shows.edit(name=f"Total Shows: {all_shows_count}")
        print(f"Updated Total Shows count: {all_shows_count}")

        # Combine series counts from all shows directories
        all_shows_count = 0
        for show_folder in ["Series", "Series2"]:
            show_path = folders.get(show_folder)
            if show_path:
                all_shows_count += count_folders(show_path)

        # Create and update sub-channels for each folder
        for folder_name, directory in folders.items():
            # Check if the folder already exists
            folder = discord.utils.get(category.channels, name=folder_name)
            if folder is None:
                # Folder doesn't exist, create it as a voice channel
                folder = await category.create_voice_channel(folder_name)
                print(f"Created folder: {folder_name} in category: {category_name}")

                # Set permissions for the folder to make it private
                await folder.set_permissions(guild.default_role, view_channel=True)
                print(f"Set permissions for {folder_name} to make it private")
            else:
                print(f"Folder {folder_name} already exists")

            # Store the channel ID if not already stored
            if folder_name not in channel_ids:
                channel_ids[folder_name] = folder.id
                print(f"Stored channel ID: {folder_name}: {folder.id}")

            # Get the count for the folder
            files_count = get_count(directory)

            # Update the sub-channel name with the count
            await folder.edit(name=f"{folder_name}: {files_count}")
            print(f"Updated {folder_name} count: {files_count}")

        await asyncio.sleep(86400)  # Update every 24 hours

# Run the bot
@bot.event
async def on_ready():
    print("Bot is ready")
    bot.loop.create_task(update_folder_counts())

bot.run(TOKEN)
