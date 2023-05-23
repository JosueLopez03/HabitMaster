from flask import Flask
from modules.player import Player
from modules.database import create_database
from modules.routes import *

app = Flask(__name__)

# Register the route functions from routes.py
app.route('/')(index)
app.route('/add', methods=['POST'])(add_habit)
app.route('/delete/<int:habit_id>', methods=['POST'])(delete_habit)
app.route('/increase_experience/<int:habit_id>', methods=['POST'])(increase_experience)
app.route('/complete/<int:habit_id>', methods=['POST'])(complete_habit)
app.route('/calendar')(calendar)

# Main
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
