from g4f.client import Client

_client = Client()

SYSTEM_PROMPT = """You are J.A.R.V.I.S., a highly advanced and professional AI assistant.
Your creator and user is Ravi. You must always address him respectfully as 'Sir'. (Never 'Sir Ravi', just 'Sir').
Your responses should be elegant, sophisticated, and heavily detailed.
CRITICAL INSTRUCTION: You must only output the exact spoken text intended for Text-to-Speech.
Do not include any formatting, markdown, asterisks for actions, emojis, or conversational filler like 'Here is the summary'.
Just provide the direct, professional spoken dialogue."""

def summarize_email(sender, subject, body):
    """Use g4f GPT-4o to produce a highly concise summary of an email."""
    prompt = (
        "Provide a concise, 2-3 sentence summary of this email for Sir. "
        "You must mention who sent it, the main topic, and the key takeaways or action items. "
        "Keep it brief but informative in the style of J.A.R.V.I.S.\n\n"
        f"From: {sender}\n"
        f"Subject: {subject}\n"
        f"Body:\n{body}"
    )
    try:
        response = _client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[AI] Summarize error: {e}")
        return f"Sir, you have a new email from {sender} regarding {subject}. I am currently unable to generate a detailed summary."


def detail_email(sender, subject, body):
    """Use g4f GPT-4o to produce a thorough, detailed explanation of an email."""
    prompt = (
        "Provide a fully comprehensive, heavily detailed reading and analysis of this email for Sir. "
        "Read out all important points, action items, deadlines, and context.\n\n"
        f"From: {sender}\n"
        f"Subject: {subject}\n"
        f"Body:\n{body}"
    )
    try:
        response = _client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[AI] Detail error: {e}")
        return f"Sir, you have a new email from {sender} regarding {subject}. I am currently unable to generate a detailed analysis."


def generate_reminder():
    """Use g4f GPT-4o to produce a short TTS reminder."""
    prompt = (
        "Generate a short, professional reminder to tell Sir that a new email is awaiting his attention. "
        "CRITICAL: Do NOT mention the sender, subject, or content of the email. "
        "Just gently and professionally inform him that a new email has arrived and requires his attention."
    )
    try:
        response = _client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[AI] Reminder error: {e}")
        return "Sir, a new email has arrived and requires your attention."
