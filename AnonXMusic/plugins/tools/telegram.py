from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from AnonXMusic import botxx

# Quiz questions and answers
QUIZ = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Madrid", "Rome"],
        "answer": 0,
    },
    {
        "question": "Who wrote 'Hamlet'?",
        "options": ["William Shakespeare", "Charles Dickens", "J.K. Rowling", "Leo Tolstoy"],
        "answer": 0,
    },
    {
        "question": "What is 5 + 3?",
        "options": ["5", "8", "10", "15"],
        "answer": 1,
    },
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await update.message.reply_text("Welcome to the Quiz Bot! Type /quiz to start the quiz.")

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the quiz."""
    context.user_data['current_question'] = 0
    context.user_data['score'] = 0
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the current question to the user."""
    question_index = context.user_data['current_question']
    question = QUIZ[question_index]

    # Create inline keyboard options
    keyboard = [
        [InlineKeyboardButton(option, callback_data=str(i))]
        for i, option in enumerate(question['options'])
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the question
    if update.message:
        await update.message.reply_text(question['question'], reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(question['question'], reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles user's answer."""
    query = update.callback_query
    await query.answer()

    question_index = context.user_data['current_question']
    question = QUIZ[question_index]

    # Check if the answer is correct
    selected_option = int(query.data)
    if selected_option == question['answer']:
        context.user_data['score'] += 1
        response = "Correct!"
    else:
        response = f"Wrong! The correct answer was: {question['options'][question['answer']]}"

    # Move to the next question or end the quiz
    context.user_data['current_question'] += 1
    if context.user_data['current_question'] < len(QUIZ):
        await query.message.reply_text(response)
        await send_question(update, context)
    else:
        total_score = context.user_data['score']
        await query.message.reply_text(
            f"{response}\n\nQuiz finished! Your score: {total_score}/{len(QUIZ)}"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    await update.message.reply_text("Use /start to begin and /quiz to start the quiz.")

# Handlers
start_handler = CommandHandler("start", start)
quiz_handler = CommandHandler("quiz", start_quiz)
help_handler = CommandHandler("help", help_command)
callback_query_handler = CallbackQueryHandler(handle_answer)
