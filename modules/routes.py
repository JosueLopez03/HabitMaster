from flask import render_template, request, redirect, url_for, jsonify
from datetime import datetime
import sqlite3
from modules.player import Player
from modules.database import DB_NAME

TOP_HABITS = [
    "Exercise for 60 minutes",
    "Eat a balanced meal",
    "Drink the recommended amount of water",
    "Sleep for 7-9 hours",
    "Practice a stress management activity",
    "Practice good hygiene",
    "Limit social media",
    "Engage in a hobby for 30 minutes",
    "Practice a new skill"
]

player = Player()

# Routes
def index():
    # Retrieve habits from the database
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM habits')
        habits = c.fetchall()

    return render_template('index.html', habits=habits, top_habits=TOP_HABITS, enumerate=enumerate, player=player)

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

def delete_habit(habit_id):
    # Delete habit from the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

def increase_experience(habit_id):
    # Increase the player's experience
    player.increase_experience()

    # Delete habit from the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

def complete_habit(habit_id):
    completed = request.form.get('completed')

    # Update habit completion status in the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE habits SET completed = ? WHERE id = ?', (int(completed), habit_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

def calendar():
    # Get the current year and month
    now = datetime.now()
    year = now.year
    month = now.month
    return render_template('calendar.html', year=year, month=month)
