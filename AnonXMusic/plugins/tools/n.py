import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from dotenv import load_dotenv
from AnonXMusic import app

# Load environment variables from a .env file
load_dotenv()

# MongoDB URI from .env file
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://jay:jay@jay.r2lxx.mongodb.net/?retryWrites=true&w=majority&appName=jay")


# MongoClient to interact with MongoDB
client = MongoClient(MONGO_DB_URI)

# Backup MongoDB database function (used with /export)
def backup_mongo_db():
    try:
        # Create a temporary backup file in memory using a pipe
        result = subprocess.run(
            ['mongodump', '--uri', MONGO_DB_URI, '--archive', '--gzip'],
            capture_output=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
        return None

# Restore MongoDB database function using mongoimport
def restore_mongo_db(backup_file_path):
    try:
        # Import data back into the new database
        subprocess.run(
            ['mongoimport', '--uri', MONGO_DB_URI, '--file', backup_file_path, '--drop'],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during restore: {e}")
        return False

# Command handler for /import
@app.on_message(filters.command("nimport"))
async def import_backup(client, message: Message):
    # Check if a file is provided with the command
    if message.document:
        # Get the file path and download the file
        file = message.document
        file_path = await message.download()

        # Process backup restoration
        success = restore_mongo_db(file_path)
        if success:
            await message.reply("Backup has been successfully imported to the new MongoDB database.")
        else:
            await message.reply("There was an error while importing the backup.")
    else:
        await message.reply("Please send a valid MongoDB backup file with the /import command.")

# Command handler for /export (backup command)
@app.on_message(filters.command("nexport"))
async def export_database(client, message: Message):
    # Perform MongoDB backup
    backup_data = backup_mongo_db()

    if backup_data:
        # Send the backup data to the user as a file (in memory)
        await message.reply_document(
            document=backup_data,
            filename="backup.gz",
            caption="Here is your MongoDB backup"
        )
    else:
        await message.reply("There was an error during the backup process.")
