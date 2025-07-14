import os
from openai import OpenAI

# Always use environment variables for API keys
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Correct model name and remove invalid 'store' parameter
completion = client.chat.completions.create(
  model="gpt-4o",  # Corrected model name
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

# Properly formatted print statement
print(completion.choices[0].message.content)