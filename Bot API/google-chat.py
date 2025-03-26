from chatterbot import ChatBot
chatbot = ChatBot("MyChatbot")
exit_conditions = (":q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"Chatbot: {chatbot.get_response(query)}")
