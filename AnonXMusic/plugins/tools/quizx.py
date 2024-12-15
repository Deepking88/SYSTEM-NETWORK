from AnonXMusic import app 
from pyrogram import Client

@app.on_message()
async def send_poll(client, message):
    if message.text == "/poll":  # Command to trigger poll creation
        # Define options as a list of strings
        options = ["Option 1", "Option 2", "Option 3"]  # List of answer options

        # Send the poll with the given question and options
        await client.send_poll(
            chat_id=message.chat.id,  # The chat ID where the poll will be sent
            question="What's your favorite option?",  # The poll question
            options=options,  # The list of options as strings
            is_anonymous=True  # Whether the poll is anonymous or not
        )
