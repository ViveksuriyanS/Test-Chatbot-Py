import sqlite3
import re
import requests
from ollama import chat
from ollama import ChatResponse

#Configurations
LOG_FILE_PATH="/Users/vs032332/Documents/chatbot/vmware_vrlcm.log"
CHATBOT_API_URL="https://api.restful-api.dev/objects/6"

#Initialize database
def init_db():
	conn = sqlite3.connect('test.db') # For creating Database
#	conn = sqlite3.connect(':error:') # For creating Table
	print("Database connection is successful" , conn.total_changes) # For printing the connection status
	cursor = conn.cursor() # Cursor is used for executing the queries
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_message TEXT UNIQUE,
            kb_article TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )		
	'''
	)
	print(conn.total_changes)
	conn.commit()
	conn.close()

# Generate Response
def generate_response_from_ai(error_code):
	response: ChatResponse = chat(model='llama3.2', messages=[
	  {
	    'role': 'user',
	    'content': error_code,
	  },
	])
	print(response['message']['content'])

# For access fields directly from the response object
print(response.message.content)


# Extract errors from log file
def error_extract(log_text):
	print("In extract_error")
	error_pattern = r"ERROR(.+)"
	return set(re.findall(error_pattern, log_text))

# Process log file
def process_log():
	print("In process_log")
	with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
		log_content = file.read()
	errors = error_extract(log_content)
	for error in errors:
		if is_error_new(error):
			kb_article = get_kb_article(error)
			store_error(error,kb_article)
			print(f"Error:  {error} -> KB Article: {kb_article}")
			
			generate_response_from_ai(error)
			print(f"")

# Check if it is new error
def is_error_new(error_message): 
	# For creating Database
	conn = sqlite3.connect('test.db')
	cursor = conn.cursor()
	cursor.execute('SELECT 1 from errors where error_message = ?', (error_message,))
	result = cursor.fetchone()
	conn.close()
	return result is None

# Get KB Article
def get_kb_article(error_message):
	response = requests.post(CHATBOT_API_URL,json={"error": error_message})
	return response.json().get("kb_article", "No KB article found.")

# Store error
def store_error(error_message, kb_article):
	conn = sqlite3.connect('test.db') # For creating Database
	cursor = conn.cursor()
	cursor.execute("INSERT INTO errors (error_message, kb_article) VALUES (?, ?)", (error_message, kb_article))
	conn.commit()
	conn.close()

#Main Class
init_db()
process_log()
