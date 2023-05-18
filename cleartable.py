import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Delete all rows from table
c.execute('DELETE FROM users;',);

print('We have deleted', c.rowcount, 'records from the table.')

# Commit the changes to db
conn.commit()
# Close the connection
conn.close()
