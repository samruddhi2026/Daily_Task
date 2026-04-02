import os
import json
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


choice = input("Enter 1 for text input or 2 for file input: ")


if choice == "1":
    resume_text = input("Enter your resume text:\n")

elif choice == "2":
    file_name = input("Enter file name (example: resume.txt): ")
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            resume_text = f.read()
    except:
        print("File not found")
        exit()
else:
    print("Invalid choice")
    exit()


prompt = f"""
You are an AI Resume Screening System.

Your role is to analyze a resume and determine whether the candidate is eligible for a job role based strictly on the given information.

STRICT RULES:
- Do NOT assume anything
- Do NOT add explanation outside JSON
- Do NOT guess missing data
- Output ONLY valid JSON

OUTPUT FORMAT:
{{
    "name": "string",
    "skills": ["list of skills"],
    "eligibility": "Eligible / Not Eligible"
}}

LOGIC:
- Extract candidate name
- Extract skills from resume (do NOT rely on predefined list)

- If candidate has relevant technical or professional skills → "Eligible"
- If candidate has very weak or no skills → "Not Eligible"

FEW-SHOT EXAMPLES:

Input:
Name: A
Skills: Python, SQL
Output:
{{"name": "A", "skills": ["Python", "SQL"], "eligibility": "Eligible"}}

Input:
Name: B
Skills: Communication
Output:
{{"name": "B", "skills": ["Communication"], "eligibility": "Eligible"}}

Input:
Name: C
Skills: None
Output:
{{"name": "C", "skills": [], "eligibility": "Not Eligible"}}

ANTI-PROMPT:
- Do NOT explain reasoning
- Do NOT add extra text
- Do NOT assume skills not mentioned

Now analyze this resume:

{resume_text}
"""


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={"response_mime_type": "application/json"}
)


try:
    result = response.parsed if response.parsed else json.loads(response.text)
except:
    print("Error: Invalid JSON response")
    exit()


print("\nOutput:\n")
print(json.dumps(result, indent=4))