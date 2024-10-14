from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, static_folder='../front-end', template_folder='../front-end')

# Database configuration
DATABASE_CONFIG = {
    'user': 'admin',  # Change according to your database username
    'password': '',  # Your database password
    'host': '',  # Change according to your database host
    'database': 'telefonkatalog'  # The database name
}

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(**DATABASE_CONFIG)

# Create the table if it doesn't exist
def create_table_if_not_exists():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS personer (
                            fornavn VARCHAR(255),
                            etternavn VARCHAR(255),
                            telefonnummer VARCHAR(20)
                        )''')
        conn.commit()
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    fornavn = request.form.get('fornavn')
    etternavn = request.form.get('etternavn')
    telefonnummer = request.form.get('telefonnummer')

    # Add new person to the database
    add_person_to_db(fornavn, etternavn, telefonnummer)

    return f'{fornavn} {etternavn} has been added with the phone number {telefonnummer}.'

# Function to add a new person to the database
def add_person_to_db(fornavn, etternavn, telefonnummer):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personer (fornavn, etternavn, telefonnummer) VALUES (%s, %s, %s)",
                       (fornavn, etternavn, telefonnummer))
        conn.commit()
    except Error as e:
        print(f"Error adding person: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/view', methods=['GET'])
def view_all():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personer")
        resultater = cursor.fetchall()

        if not resultater:
            return "No registered persons in the catalog."
        else:
            output = "<h2>Registered Persons:</h2>"
            for person in resultater:
                output += f"<p>Fornavn: {person[0]}, Etternavn: {person[1]}, Telefonnummer: {person[2]}</p>"
            return output
    except Error as e:
        return f"Error fetching persons: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    create_table_if_not_exists()  # Ensure the table is created before running the app
    app.run(debug=True)
