from pyrogram import Client, filters
from AnonXMusic import app

# Define the function to send a poll
@app.on_message(filters.command("poll"))
async def send_poll(client, message):
    # Sending a poll when the "/send_poll" command is received
    await app.send_poll(
        chat_id=message.chat.id,  # The chat ID (group or private chat)
        question="Is this a poll question?",  # Poll question
        options=["Yes", "No", "Maybe"]  # Poll options
    )
