import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from PyPDF2 import PdfReader  # For extracting text from PDF
from AnonXMusic import app

async def extract_pdf_text(file_path):
    """Extract text from a PDF file using PyPDF2."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()  # Extract text from each page
    return text


@app.on_message(filters.document)
async def handle_pdf(client, message: Message):
    """Handle the received PDF document and create a poll."""
    
    # Check if the document is a PDF
    if message.document.mime_type != "application/pdf":
        await message.reply("Please send a valid PDF file.")
        return
    
    # Download the PDF file using the correct method
    file_path = await client.download_media(message.document.file_id)

    # Extract text from the PDF
    text = extract_pdf_text(file_path)

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
