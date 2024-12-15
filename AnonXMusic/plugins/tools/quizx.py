import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, PollOption
from pyrogram.enums import PollType
from datetime import datetime
from AnonXMusic import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define your quiz question and options
QUESTION = "What is the capital of France?"
OPTIONS = ["Berlin", "Madrid", "Paris", "Rome"]
CORRECT_OPTION_ID = 2  # 0-based index of the correct answer (Paris)


# Start command to send the quiz poll
@app.on_message(filters.command("nstart"))
async def start_quiz(client, message):
    # Send the quiz as a poll
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Start Quiz", callback_data="start_quiz")]]
    )
    
    await message.reply_text(
        "Welcome to the quiz bot! Click below to start the quiz.",
        reply_markup=keyboard
    )

# Function to send a quiz poll when the button is clicked
@app.on_callback_query(filters.regex("start_quiz"))
async def send_quiz(client, callback_query):
    # Send a poll (quiz) to the user
    poll_message = await callback_query.message.reply_poll(
        QUESTION,
        options=OPTIONS,
        type=PollType.QUIZ,
        correct_option_id=CORRECT_OPTION_ID,
        explanation="Paris is the capital of France.",
        is_anonymous=True,
        allows_multiple_answers=False
    )
    # Acknowledge the callback query to remove the loading state
    await callback_query.answer()

# Handle poll answers
@Client.on_poll_answer()
async def poll_answer(client, poll_answer):
    # Get the answer details
    chosen_option_id = poll_answer.option_ids[0]
    user_id = poll_answer.user.id

    # Check if the answer is correct
    if chosen_option_id == CORRECT_OPTION_ID:
        result = "Correct!"
    else:
        result = "Incorrect. The correct answer is Paris."

    # Send the result to the user
    await client.send_message(
        user_id,
        f"Your answer: {OPTIONS[chosen_option_id]}\n{result}"
    )
