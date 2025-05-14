import openai
from django.conf import settings

openai.api_key = settings.GROQ_API_KEY

openai.api_base = "https://api.groq.com/openai/v1"  # ✅ Correct for Groq

def get_ai_recommendations(user_books):
    # Prepare the prompt with the user's borrowed books
    titles = ', '.join(user_books)
    messages = [
        {"role": "system", "content": "You are a helpful library assistant."},
        {"role": "user", "content": f"I've borrowed these books: {titles}. Recommend 5 similar books. Only give the book titles as a numbered list."}
    ]

    response = openai.ChatCompletion.create(
        model="llama3-70b-8192",  # or any other supported Groq model
        messages=messages,
        temperature=0.7,
        max_tokens=200
    )


    return response['choices'][0]['message']['content'].strip()
