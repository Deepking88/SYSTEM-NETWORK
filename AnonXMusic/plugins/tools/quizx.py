import asyncio
from telethon import TelegramClient, events, types
from AnonXMusic import botx 

# Define your poll question and options
QUESTION = "What is the capital of France?"
OPTIONS = ["Berlin", "Madrid", "Paris", "Rome"]
CORRECT_OPTION_ID = 2  # Index for "Paris"


# Handler for the /quiz command
@botx.on(events.NewMessage(pattern='/los'))
async def send_quiz(event):
    # Sending a poll (quiz) to the user
    poll = await event.respond(
        QUESTION,
        buttons=None,  # Optional: can be used for inline buttons, not required for poll
        poll=types.Poll(
            question=QUESTION,
            answers=[types.PollAnswer(option) for option in OPTIONS],
            correct_option=CORRECT_OPTION_ID,
            type=types.PollType.QUIZ,
            explanation="Paris is the capital of France."
        )
    )
    await event.reply("Quiz sent!")

# Handler to listen for incoming poll answers
@botx.on(events.NewMessage)
async def handle_poll_answer(event):
    if event.poll is not None:
        answer = event.poll
        if event.message.poll_answer.selected_id == CORRECT_OPTION_ID:
            await event.reply("Correct!")
        else:
            await event.reply("Incorrect!")
