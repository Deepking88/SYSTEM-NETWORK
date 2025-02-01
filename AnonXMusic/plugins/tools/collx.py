import os
import json
from pymongo import MongoClient
from pyrogram import Client, filters
from PURVIMUSIC import app

# MongoDB connection setup
MONGODB_URI = "mongodb+srv://jay:jay@jay.r2lxx.mongodb.net/?retryWrites=true&w=majority&appName=jay"  # Update to your MongoDB URI

client = MongoClient(MONGODB_URI)


@app.on_message(filters.command("trans"))
def import_data(client, message):
    # Check if a file was sent
    if message.reply_to_message and message.reply_to_message.document:
        file_id = message.reply_to_message.document.file_id
        file_path = client.download_media(file_id)

        try:
            with open(file_path, 'r') as file:
                backup_data = json.load(file)  # Assumes your backup is in JSON format
                
            # Bulk insert data to MongoDB
            if isinstance(backup_data, list):
                client.mongodb_backup.data.insert_many(backup_data)
            else:
                client.mongodb_backup.data.insert_one(backup_data)

            message.reply_text("Data imported successfully!")
        except Exception as e:
            message.reply_text(f"Failed to import data: {str(e)}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)  # Clean up the downloaded file
    else:
        message.reply_text("Please reply to a message with a file.")

@app.on_message(filters.command("nstart"))
def start(client, message):
    message.reply_text("Welcome! Use /import_data to import data from a backup file.")
