from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DB_NAME = 'habitmaster.db'

def create_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create habit table
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    # Retrieve habits from the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM habits')
    habits = c.fetchall()
    conn.close()

    return render_template('index.html', habits=habits)

@app.route('/add', methods=['POST'])
def add_habit():
    habit_name = request.form.get('habit_name')

    # Insert new habit into the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO habits (name) VALUES (?)', (habit_name,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/complete/<int:habit_id>')
def complete_habit(habit_id):
    # Update habit completion status in the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE habits SET completed = 1 WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Main
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
