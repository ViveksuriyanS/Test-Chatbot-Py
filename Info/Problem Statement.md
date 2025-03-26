Problem Statement
* Whenever a customer faces an error, it will become unnoticed, as the logs are being logged in the background
    -> What if we have an AI agent that monitors the health of the VMs deployed, 
    -> What if whenever an error has occurred, customer gets notified about the issue and the reason behind it
    -> What if the customer has ended up in failed state, by providing wrong information
    -> What if for the known issues, customer can troubleshoot themself.

By introducing the chat assistant, it will become an 

ChatBot: Python program
Note: Should be a standalone service. [If inside another service, could fail]
1. Foreground: Service that runs to respond the customer query
2. Background: Also checks for the logs. Current POC - VRSLCM logs
    -> Trigger Log Check and return 
3. Background: Also checks for the system health. POC - VRSLCM, VROPS
4. Background: Check for any spike. Future POC
5. 

Working
1. When application runs, the logs will be logged in a file
2. This log file will be the target [Multiple file can be introduced]
3. Grep for error message
4. With the error message and error code available
    * Check in DB, with error code and error message
        -> If error not present : Store it in DB, with KB article or without 
        -> If error exist : KB article found, then provide KB article. 
5. Configure a cron job, that runs every 5 to 10 mins
6. Handle a logic to eliminate the duplicate processing of same logs again [Based on Time Stamp or Line number]
7. 


pip3 install chatterbot
pip3 install chatterbot_corpus



SQLITE3 commands

# To connect
sqlite3 test1.db

# Get all tables
.tables

# Get the table structure
pragma table_info(errors);

# Get all the elements from table errors
select * from errors;
select * from errors where id = 6;

# Update table
update errors set kb_article = 'https://knowledge.broadcom.com/external/article/314839/no-upgrade-available-message-when-attemp.html' where id = 6;

# To Exit
.exit