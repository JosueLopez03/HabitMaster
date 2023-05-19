from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DB_NAME = 'habitmaster.db'

TOP_HABITS = [
    "Exercise for 60 minutes",
    "Eat a balance meal",
    "Drink recommended amount of water",
    "Sleep for 7-9 hours",
    "Practice a stress management activity",
    "Pracitce good hygiene",
    "Limit social media",
    "Engage in a hobby for 30 minutes",
    "Practice a new skill"
]

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
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM habits')
        habits = c.fetchall()

    return render_template('index.html', habits=habits, top_habits=TOP_HABITS, enumerate=enumerate)

@app.route('/add', methods=['POST'])
def add_habit():
    selected_habit_index = int(request.form.get('habit_index'))

    if selected_habit_index < 0 or selected_habit_index >= len(TOP_HABITS):
        return redirect(url_for('index'))

    habit_name = TOP_HABITS[selected_habit_index]

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

    return jsonify({'success': True})

@app.route('/complete/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    completed = request.form.get('completed')

    # Update habit completion status in the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE habits SET completed = ? WHERE id = ?', (int(completed), habit_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})


# Main
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
