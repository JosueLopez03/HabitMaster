from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

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

class Player:
    def __init__(self):
        self.habits = []

    def add_habit(self, habit_name):
        self.habits.append(habit_name)

    def delete_habit(self, habit_name):
        self.habits.remove(habit_name)

    def get_habits(self):
        return self.habits

player = Player()

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

@app.route('/delete/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    # Delete habit from the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/complete/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    completed = request.form.get('completed')

    # Update habit completion status in the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE habits SET completed = ? WHERE id = ?', (completed, habit_id))
    conn.commit()
    conn.close()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# Main
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
