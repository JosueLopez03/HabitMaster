class Player:
    def __init__(self):
        self.habits = []
        self.level = 1
        self.experience = 0

    def add_habit(self, habit_name):
        self.habits.append(habit_name)

    def delete_habit(self, habit_name):
        self.habits.remove(habit_name)

    def get_habits(self):
        return self.habits

    def increase_experience(self):
        self.experience += 1
        if self.experience >= self.level * 5:
            self.level += 1
            self.experience = 0

    def get_level(self):
        return self.level

    def get_experience(self):
        return self.experience
    