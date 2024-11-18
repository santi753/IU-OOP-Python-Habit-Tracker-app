import sqlite3
from datetime import datetime

def see_database():
    """
    This function allows you to check the database and see the data that has been used in the program.
    """

    db_name = 'habits.db'
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('SELECT name, creation_date FROM habits')
    habits = cursor.fetchall()

    if not habits:
        print("No habits found in the database.")
        connection.close()
        return

    for habit in habits:
        name = habit[0]
        creation_date = habit[1]

        print(f"Habit name: {name}")
        print(f"Creation date: {creation_date}")

        cursor.execute('SELECT completion_date FROM habit_completions WHERE habit_name = ?', (name,))
        completions = cursor.fetchall()

        if completions:
            print("Completion date")
            for completion in completions:
                print(completion[0])
        else:
            print("No completion dates.")
        print()

    connection.close()

if __name__ == '__main__':
    see_database()
