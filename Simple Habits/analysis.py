from tabulate import tabulate
import logging
from database import Database
from habit import Habit

logger = logging.getLogger(__name__)


def table_of_habits(habits: list):
    """
    This function creates the format for a table for the habits in the database.
    The table displays the name of the habit, its creation date, its frequency,
    its periodicity, and the last time the habit was performed.

    Args:
        habits (list[Habit]): a list of all habits in the appropriate format.

    """
    if not habits:
        logger.info("No habits found.")
        print("No habits found.")
        return

    headers = ["Name", "Creation date", "Frequency", "Periodicity", "Last time done"]
    data = []
    for habit in habits:
        if habit.completion_dates:
            last_done = max(habit.completion_dates).strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_done = "Never"

        row = [
            habit.name,
            habit.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
            habit.frequency,
            habit.periodicity,
            last_done
        ]
        data.append(row)

    print(tabulate(data, headers=headers, tablefmt='grid'))


def list_all_habits(db: Database):
    """
    This function recovers all the habits from the database.

    Args:
        db (Database): use the Database.

    Returns:
        list[Habit]: a list of all habits in the database.
    """
    habits = db.show_all_habits()
    logger.info("List of all the habits.")
    return habits


def list_frequency(db: Database, frequency: str):
    """
    This function retrieves habits from the database filtered by their frequency.

    Args:
        db (Database): use the Database.
        frequency (str): desired frequency (daily or weekly).

    Returns:
        list[Habit]: a list of all habits with the desired frequency.
    """
    habits = db.show_frequency(frequency)
    logger.info(f"List all habits with frequency '{frequency}'.")
    return habits


def show_longest_streak(db: Database):
    """
    This function searches and finds the habit that has the longest streak among all the habits in the database.

    Args:
        db (Database): use the Database.

    Returns:
        Habit: the habit with the longest streak, or None if no habits have been performed or there are no habits.
    """
    habits = db.show_all_habits()
    if not habits:
        logger.info("No habits yet done.")
        return None

    # Calculate longest streaks for all habits
    max_streak = 0
    max_habit = None
    for habit in habits:
        longest_streak = habit.calculate_longest_streak()
        if longest_streak > max_streak:
            max_streak = longest_streak
            max_habit = habit

    if max_habit:
        logger.info(f"The habit '{max_habit.name}' has the longest streak of {max_streak}.")
        return max_habit
    else:
        logger.info("No habit has any streak.")
        return None


def longest_streak_for_habit(db: Database, habit_name: str):
    """
    This function searches and finds the longest streak for a specific habit.

    Args:
        db (Database): use the Database.
        habit_name (str): the name of the desired habit.

    Returns:
        int: the longest streak for the specified habit, or None if the habit doesn't exist.
    """
    habit = db.find_habit(habit_name)
    if habit:
        longest_streak = habit.calculate_longest_streak()
        logger.info(f"The longest streak for the habit '{habit.name}' is {longest_streak}.")
        return longest_streak
    else:
        logger.info(f"No habit '{habit_name}' found.")
        return None


def display_completion_dates(habit: Habit):
    """
    This feature shows the user the last seven completion dates for a specific habit.

    Args:
        habit (Habit): the habit to which completion dates are to be seen.

    """
    if not habit.completion_dates:
        logger.info(f"There are no completion dates for habit '{habit.name}'.")
        print(f"There are no completion dates for habit '{habit.name}'.")
        return

    sorted_dates = sorted(habit.completion_dates)
    last_seven_dates = sorted_dates[-7:]

    headers = ["Completion Dates"]
    data = [[date.strftime('%Y-%m-%d %H:%M:%S')] for date in last_seven_dates]
    print(f"Last completion dates for habit '{habit.name}':")
    print(tabulate(data, headers=headers, tablefmt='grid'))
    logger.info(f"The last seven end dates for the habit '{habit.name}' are shown.")


