# Define the poll sending function
from AnonXMusic import app 
from pyrogram import Client, filters, Message 

@app.on_message()
async def send_poll(client, Message: message):
    if message.text == "/poll":  # Trigger the poll with a specific command
        await client.send_poll(
            chat_id=message.chat.id,
            question="What's your favorite programming language?",
            options=["Python", "JavaScript", "C++", "Java"],
            is_anonymous=True  # Set to False for non-anonymous polls
        )
