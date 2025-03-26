from transformers import pipeline
text_generator = pipeline("text-generation", model="gpt2")
text = text_generator("The quick brown fox jumps",max_length=50, num_return_sequences=1)
print(text[0]['generated_text'])

