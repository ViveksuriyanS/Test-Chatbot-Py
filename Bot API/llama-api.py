
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key="89f6f4e7-52a9-438a-ae5c-19642141a9ce",
    base_url="https://api.llama-api.com/"
)

chat_completion = client.chat.completions.create(
    messages=[
                {
                    "role": "system",
                    "content": "You are a helpful math tutor. Guide the user through the solution step by step."
                },
                {
                    "role": "user",
                    "content": "how can I solve 8x + 7 = -23"
                }
            ],
	model="llama3-8b",    
	stream=False
)

print(chat_completion)
