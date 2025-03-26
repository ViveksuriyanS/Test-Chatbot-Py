#export OPENAI_API_KEY="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"
import openai
import os
import httpx

#client = httpx.Client(proxies=None)
#openai.api_client.transport = client

os.environ['REQUESTS_CA_BUNDLE'] = '/Users/vs032332/Downloads/CSRootCA.pem'
openai.api_key = "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"


def chat_with_gpt(prompt):
	response = openai.chat.completions.create(
		model="gpt-4-turbo",
		messages=[{"role":"user", "content": prompt}]
	)
	return response.choices[0].message.content.skip()

if __name__ == "__main__":
	while True:
		user_input = input("You: ")
		if user_input.lower() in ["quit", "exit", "bye"]:
			break
		
		response = chat_with_gpt(user_input)
		print("Chatbot:", response)
