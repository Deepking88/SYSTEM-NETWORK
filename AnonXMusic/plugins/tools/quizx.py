import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pikepdf import Pdf  # Used for extracting text from PDF
from io import BytesIO
from AnonXMusic import app

async def extract_pdf_text(file):
    """Extract text from PDF file"""
    with Pdf.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

@app.on_message(filters.document & filters.document.mime_type("application/pdf"))
async def handle_pdf(client, message: Message):
    """Handle the received PDF document and create a poll"""
    # Download the PDF file using the correct method
    pdf_file = await client.download_media(message.document.file_id)

    # Extract text from PDF
    text = await extract_pdf_text(pdf_file)

    if not text:
        await message.reply("Could not extract text from the PDF.")
        return
    
    # Split extracted text into potential questions and options (a basic approach)
    lines = text.splitlines()
    questions = []
    options = []

    for line in lines:
        if line.strip():
            # Simple rule: if line contains a "?", assume it's a question.
            if "?" in line:
                if options:
                    questions.append({"question": question, "options": options})
                question = line
                options = []
            else:
                options.append(line.strip())

    if options:
        questions.append({"question": question, "options": options})

    # Create and send polls
    for question_data in questions:
        keyboard = [
            [InlineKeyboardButton(option, callback_data=option)] 
            for option in question_data["options"]
        ]

        # Send the poll to the user
        await message.reply(
            text=f"Poll: {question_data['question']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
