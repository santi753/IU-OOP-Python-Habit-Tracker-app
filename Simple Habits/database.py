# database.py

import sqlite3
import logging
from datetime import datetime
from habit import Habit

logger = logging.getLogger(__name__)


class Database:
    """
    A class to create the database and manage the application information.
    It contains the methods to perform all the necessary operations with the database.

    Attributes:
        db_name (str): name of the SQLite database file.
        connection (sqlite3.Connection): SQLite database connection object.
        cursor (sqlite3.Cursor): cursor object for executing SQL commands.
    """

    def __init__(self, db_name='habits.db', insert_predefined=True):
        """
        Initializes the connection to the database and provides the necessary tables.

        Args:
            db_name (str, optional): give the name to the database, by default it is 'habits.db'.
            insert_predefined (bool, optional): add the predefined habits if they have not been added yet
        """
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logger.info(f"The database connection is '{self.db_name}'")
        self.create_tables()
        if insert_predefined:
            self.predefined_habits()

    def create_tables(self):
        """
        This method creates the tables needed for the application,
        it creates a table to store the habits and another to store the completion dates of the habits.
        """
        create_habits_table = '''
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            frequency TEXT,
            periodicity INTEGER,
            creation_date TEXT
        )
        '''
        create_completions_table = '''
        CREATE TABLE IF NOT EXISTS habit_completions (
            habit_name TEXT,
            completion_date TEXT,
            FOREIGN KEY(habit_name) REFERENCES habits(name)
        )
        '''
        self.cursor.execute(create_habits_table)
        self.cursor.execute(create_completions_table)
        self.connection.commit()
        logger.info("The tables were created or already existed.")

    def predefined_habits(self):
        """
        This method creates predefined habits if they do not already exist in the database.
        It creates five habits: 2 daily and 3 weekly.
        """
        self.cursor.execute('SELECT COUNT(*) FROM habits')
        count = self.cursor.fetchone()[0]
        if count == 0:
            logger.info("Creating predefined habits")
            predefined_habits = [
                Habit(name='Read', frequency='daily', periodicity=1),
                Habit(name='Meditate', frequency='daily', periodicity=2),
                Habit(name='Exercise', frequency='weekly', periodicity=3),
                Habit(name='Plan week', frequency='weekly', periodicity=1),
                Habit(name='Go to the supermarket', frequency='weekly', periodicity=1)
            ]
            for habit in predefined_habits:
                self.new_created_habit(habit)
            logger.info("The predefined habits were created")
        else:
            logger.info("The predefined habits already exist.")

    def new_created_habit(self, habit: Habit):
        """
        This method adds a new habit to the database when created by the user.

        Args:
            habit(Habit): the habit to be added to the database with its corresponding attributes.
        """
        insert_query = '''
        INSERT INTO habits (
            name, frequency, periodicity, creation_date
        ) VALUES (?, ?, ?, ?)
        '''
        habit_data = (
            habit.name,
            habit.frequency,
            habit.periodicity,
            habit.creation_date.isoformat()
        )
        try:
            self.cursor.execute(insert_query, habit_data)
            self.connection.commit()
            logger.info(f"The new habit '{habit.name}' was added to the database.")
        except sqlite3.IntegrityError:
            logger.info(f"The habit created '{habit.name}' already exists.")

    def delete_habit(self, habit_name: str):
        """
        This method removes a habit from the database if the user wants to

        Args:
            habit_name (str): the habit to be removed from the database.
        """
        delete_completions_query = 'DELETE FROM habit_completions WHERE habit_name = ?'
        delete_habit_query = 'DELETE FROM habits WHERE name = ?'
        self.cursor.execute(delete_completions_query, [habit_name])
        self.cursor.execute(delete_habit_query, [habit_name])
        self.connection.commit()
        if self.cursor.rowcount > 0:
            logger.info(f"The habit '{habit_name}' was deleted.")
        else:
            logger.info(f"The habit '{habit_name}' does not exist.")

    def add_completion(self, habit_name: str, completion_date: datetime):
        """
        This method adds to the database the date of completion of the habit, when the user performs it.

        Args:
            habit_name (str): the name of the habit that has been performed.
            completion_date (datetime): the date and time the habit was performed.
        """
        insert_query = '''
        INSERT INTO habit_completions (
            habit_name, completion_date
        ) VALUES (?, ?)
        '''
        completion_data = (
            habit_name,
            completion_date.isoformat()
        )
        self.cursor.execute(insert_query, completion_data)
        self.connection.commit()
        logger.info(f"The habit '{habit_name}' was made on {completion_date}.")

    def get_completions(self, habit_name: str):
        """
        This method displays completion dates for a specific habit if the user wants to check them.

        Args:
            habit_name (str): the name of the habit for which the user wants to check the completion dates.

        Returns:
            list[datetime]: a list of completion dates for the desired habit.
        """
        select_query = 'SELECT completion_date FROM habit_completions WHERE habit_name = ?'
        self.cursor.execute(select_query, [habit_name])
        rows = self.cursor.fetchall()
        completion_dates = [datetime.fromisoformat(row[0]) for row in rows]
        return completion_dates

    def find_habit(self, habit_name: str):
        """
        This method finds a specific habit in the database

        Args:
            habit_name (str): the name of the habit to find.

        Returns:
            Habit: the specific habit, if the habit is not found it returns None
        """
        select_query = 'SELECT * FROM habits WHERE name = ?'
        self.cursor.execute(select_query, [habit_name])
        row = self.cursor.fetchone()
        if row:
            habit = Habit(name=row[0], frequency=row[1], periodicity=row[2])
            habit.creation_date = datetime.fromisoformat(row[3])
            habit.completion_dates = self.get_completions(habit.name)
            logger.debug(f"The habit '{habit_name}' was found in the database.")
            return habit
        else:
            logger.info(f"The habit '{habit_name}' was not found in the database.")
            return None

    def show_all_habits(self):
        """
        This method shows all the habits in the database.

        Returns:
            list[Habit]: a list of all the habits in the database.
        """
        select_query = 'SELECT * FROM habits'
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()
        habits = []
        for row in rows:
            habit = Habit(name=row[0], frequency=row[1], periodicity=row[2])
            habit.creation_date = datetime.fromisoformat(row[3])
            habit.completion_dates = self.get_completions(habit.name)
            habits.append(habit)
        logger.info("Show all habits.")
        return habits

    def show_frequency(self, frequency: str):
        """
        This method shows a list of habits with the specific frequency that the user wants to see.

        Args:
            frequency (str): the frequency the user wants to see (daily or weekly).

        Returns:
            list[Habit]: a list of habits that have the desired frequency.
        """
        select_query = 'SELECT * FROM habits WHERE frequency = ?'
        self.cursor.execute(select_query, [frequency])
        rows = self.cursor.fetchall()
        habits = []
        for row in rows:
            habit = Habit(name=row[0], frequency=row[1], periodicity=row[2])
            habit.creation_date = datetime.fromisoformat(row[3])
            habit.completion_dates = self.get_completions(habit.name)
            habits.append(habit)
        logger.info(f"Show all habits with frequency '{frequency}'.")
        return habits

    def exit(self):
        """
        Close the database connection.
        """
        self.connection.close()
        logger.info(f"The connection with '{self.db_name}' is closed.")


