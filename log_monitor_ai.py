import os
import re
import time
import ollama
import sqlite3
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configurations
LOG_FILE_PATH = "/Users/vs032332/Documents/chatbot/vmware_vrlcm_Test.log"
FILE_WATCH_PATH = ""
CHATBOT_API_URL = "https://api.restful-api.dev/objects/6"

# Initialize database
def init_db():
    conn = sqlite3.connect("test1.db")  # For creating Database
    # 	conn = sqlite3.connect(':error:') # For creating Table
    print(
        "Database connection is successful", conn.total_changes
    )  # For printing the connection status
    cursor = conn.cursor()  # Cursor is used for executing the queries
    cursor.execute(
        """
	CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_message TEXT UNIQUE,
            kb_article TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )		
	"""
    )
    print(conn.total_changes)
    conn.commit()
    conn.close()


# Generate Response
def generate_response_from_ai(error_code):
    error = error_code.split("--")[1]
    print(f"KB Article not found. Generating the error message for {error}...")
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": error,
            },
        ],
    )
    print(response["message"]["content"])
    return response["message"]["content"]


# For access fields directly from the response object
# print(response.message.content)


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
        print("_______________________________________________________________________________________________________________")
        if is_error_new(error):
            response = generate_response_from_ai(error)
            store_error(error, response)
            print(f"")
        else:
            kb_article = get_kb_article(error)
            if "No KB article found." in kb_article:
                response = generate_response_from_ai(error)
                update_error(error, response)
                print(f"")
            else:
                print(f"Error:  {error} -> KB Article: {kb_article}")


# Check if it is new error
def is_error_new(error_message):
    # For creating Database
    conn = sqlite3.connect("test1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 from errors where error_message = ?", (error_message,))
    result = cursor.fetchone()
    conn.close()
    return result is None


# Get KB Article
def get_kb_article(error_message):
    # For creating Database
    conn = sqlite3.connect("test1.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT kb_article from errors where error_message = ?", (error_message,)
    )
    result = cursor.fetchone()
    conn.close()
    # response = requests.post(CHATBOT_API_URL, json={"error": error_message})
    # return response.json().get("kb_article", "No KB article found.")
    return result

# Update Error
def update_error(error_message, kb_article):
    conn = sqlite3.connect("test1.db")  # For creating Database
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE errors set kb_article = (?) where error_message = (?)", (kb_article, error_message)
    )
    conn.commit()
    conn.close()
    
# Store error
def store_error(error_message, kb_article):
    conn = sqlite3.connect("test1.db")  # For creating Database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO errors (error_message, kb_article) VALUES (?, ?)",(error_message, kb_article),)
    conn.commit()
    conn.close()
    
# Watchdog handler to monitor log file changes
class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == LOG_FILE_PATH:
            print("Log file updated. Processing new logs...")
            process_log()

# Start monitoring log files
def start_monitoring():
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(LOG_FILE_PATH), recursive=True)
    observer.start()
    print(f"Monitoring log file: {LOG_FILE_PATH}")
    try:
        while True:
             time.sleep(60)  # Check logs every 1 minute
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Main Class
init_db()
process_log()
start_monitoring()
