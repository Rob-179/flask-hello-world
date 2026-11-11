import os
import psycopg2
from flask import Flask

app = Flask(__name__)

# connect to the postgreSQL database
def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])
# Homepage

@app.route('/')
def hello_world():
    return 'Hello World from Robert Edwards in 3308'

# Test database connection

@app.route('/db_test')
def db_test():
    conn = get_connection()
    conn.close()

    return 'Database connection successful'

# Create basketball table

@app.route('/db_create')
def db_create():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Basketball (
            First VARCHAR(255),
            Last VARCHAR(255),
            City VARCHAR(255),
            Name VARCHAR(255),
            Number INT 
        );
    ''')

    conn.commit()
    cur.close()
    conn.close()

    return 'Basketball Table Created'

# Insert basketball players

@app.route('/db_insert')
def db_insert():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO Basketball (First, Last, City, Name, Number)
        VALUES
            ('Jayson', 'Tatum', 'Boston', 'Celtics', 0),
            ('Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
            ('Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
            ('Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2);
        ''')

    conn.commit()
    cur.close()
    conn.close()

    return 'Basketball Table Populated'


# Query and display basketball players

@app.route('/db_select')
def db_select():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM Basketball;')
    records = cur.fetchall()

    cur.close()
    conn.close()

    #HTML table 

    response = '<table border="1">'
    response += '<tr><th>First</th><th>Last</th><th>City</th><th>Name</th><th>Number</th></tr>'

    for record in records:
        response += '<tr>'
        for value in record:
            response += f'<td>{value}</td>'
        response += '</tr>'

    response += '</table>'

    return response

# Drop Basketball table

@app.route('/db_drop')
def db_drop():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('DROP TABLE Basketball;')
    conn.commit()
    cur.close()
    conn.close()

    return 'Basketball Table Dropped'
    