import re
from datetime import datetime, timedelta
import requests

# LLM endpoint
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

def query_llm_local_or_api(prompt):
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(LM_STUDIO_URL, json=payload)
    response.raise_for_status()

    result = response.json()
    return result['choices'][0]['message']['content']

# AI Suggestion Engine
def generate_ai_suggestions(task_data, context_entries):
    full_context = " ".join([c["content"] for c in context_entries])
    prompt = f"""
You are a productivity assistant. Analyze the following context:
{full_context}

Now, given this task:
Title: {task_data['title']}
Description: {task_data['description']}

Provide:
1. Priority score (0–10)
2. Enhanced description
3. Recommended category
4. Deadline suggestion
5. 🔍 Sentiment summary of context
6. 🔑 Top 5 keywords from context
"""

    response = query_llm_local_or_api(prompt)

    print("=== RAW LLM RESPONSE ===")
    print(response)

    return {
        "priority": extract_number(response),
        "enhanced_description": extract_section(response, "Enhanced description"),
        "deadline": extract_date(response),
        "category": extract_category(response),
        "sentiment": extract_section(response, "Sentiment summary"),
        "keywords": extract_section(response, "Top 5 keywords"),
    }

# Extract a number like: 1. Priority score: 7
def extract_number(text):
    match = re.search(r'priority.*?:\s*(\d{1,2})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    match = re.findall(r'\b([1-9]|10)\b', text)
    if match:
        return int(match[0])

    return 5  # default fallback priority

# Extract date from LLM response or fallback
def extract_date(text):
    # Try strict YYYY-MM-DD first
    match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if match:
        return match.group(1)

    # Try relaxed natural language dates like "July 7", "7 July"
    match = re.search(r'(\d{1,2})[ ]?(?:st|nd|rd|th)?[ ]?(January|February|March|April|May|June|July|August|September|October|November|December)', text, re.IGNORECASE)
    if match:
        try:
            dt = datetime.strptime(f"{match.group(1)} {match.group(2)} {datetime.now().year}", "%d %B %Y")
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    # Default fallback = 3 days from today
    return (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

# Extract section by heading like "Enhanced description:"
def extract_section(text, heading):
    pattern = rf"{heading}.*?:\s*(.*?)(?:\n\d\.|\n\n|\Z)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""

# Extract category name
def extract_category(text):
    match = re.search(r'category.*?:\s*([A-Za-z ]+)', text, re.IGNORECASE)
    return match.group(1).strip().capitalize() if match else "General"
