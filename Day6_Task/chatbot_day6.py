import os
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Set GEMINI_API_KEY in your environment before running this script.")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a friendly technical recruiter chatbot.

Conversation flow rules:
1. Start with a warm greeting before asking anything.
2. Ask only one short and easy question at a time.
3. Begin with simple background questions like name, interest, skills, or experience.
4. Do not ask hard technical questions at the beginning.
5. If the user says "no", "not interested", "skip", or gives a negative reply, politely move to the next easy question.
6. Keep the tone supportive, natural, and brief.
7. Do not criticize the user.
8. After a few easy questions, you may gradually ask slightly more technical questions.
"""

messages = [{"role": "system", "content": system_prompt}]


def trim_messages(memory):
    system_message = memory[0]
    recent_messages = memory[1:]
    max_messages = 10
    if len(recent_messages) > max_messages:
        recent_messages = recent_messages[-max_messages:]
    memory[:] = [system_message] + recent_messages


def build_gemini_contents(memory):
    contents = []
    for message in memory[1:]:
        role = "model" if message["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": message["content"]}]})
    return contents


def clean_reply(text):
    return re.sub(r"\s+", " ", text).strip()


opening_message = (
    "Hello! Welcome to the recruiter bot. "
    "Let's start with a few easy questions. What should I call you?"
)

print(f"Recruiter: {opening_message}")
messages.append({"role": "assistant", "content": opening_message})

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit" or user_input.lower() == "stop":
        print("Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})
    trim_messages(messages)

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=build_gemini_contents(messages),
        config={"system_instruction": system_prompt}
    )

    assistant_reply = clean_reply(response.text)
    print(f"Recruiter: {assistant_reply}\n")

    messages.append({"role": "assistant", "content": assistant_reply})
    trim_messages(messages)
