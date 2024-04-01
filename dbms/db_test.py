import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Function to execute a query and print the output
def execute_query(query):
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        print("No Output")
    for row in rows:
        print(row)

# Prompt the user for queries until they choose to exit
while True:
    query = input("Enter a query (or 'exit' to quit): ")
    if query == 'exit':
        break
    execute_query(query)

# Close the database connection
conn.close()