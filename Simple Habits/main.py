# main.py


import click
import logging
from habit import Habit
from database import Database
import analysis
import sys

logging.basicConfig(
    filename='habit_tracker.log',
    level=logging.INFO,
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s'
)
logger = logging.getLogger(__name__)

db = Database()


def create_habit():
    """
    This function allows the user to create a new habit. The user must indicate the name, frequency and periodicity
    of the habit he wants to perform. The habit is saved in the database when it is created.
    """
    while True:
        name = click.prompt('Enter the name of the new habit').strip()
        if not name:
            click.echo("Please enter the name of the habit.")
            logger.info("User input is empty")
            continue
        if name.isdigit():
            click.echo("Please enter a valid name.")
            logger.info(f"The user entered an incorrect habit name: {name}")
            continue
        break

    frequency = click.prompt(
        'How often do you plan to do this habit?',
        type=click.Choice(['daily', 'weekly'], case_sensitive=False)
    )
    periodicity = click.prompt(
        'How many times are you going to perform the habit in that period?',
        type=click.IntRange(1, 20)
    )
    habit = Habit(name=name, frequency=frequency.lower(), periodicity=periodicity)
    db.new_created_habit(habit)
    logger.info(f"The habit '{habit.name}' was created.")
    click.echo(f"You have decided to commit to the habit '{name}'. Congratulations, you can do it!")
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def delete_habit():
    """
    This function allows the user to choose a habit that they no longer want to do and delete it from the database.
    """
    habits = db.show_all_habits()
    if not habits:
        click.echo('The habit to delete has not been found.')
        logger.info("There is no habit to delete")
        click.prompt('Press Enter to return to the main menu', default='', show_default=False)
        return

    click.echo('You have these habits:')
    for x, habit in enumerate(habits, start=1):
        click.echo(f"{x}. {habit.name}")

    while True:
        try:
            choice = click.prompt('Choose the number of the habit you want to eliminate', type=int)
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                break
            else:
                click.echo('Please select a habit number from the list.')
                logger.info(f"Invalid habit selection: {choice}")
        except (ValueError, TypeError):
            click.echo('Invalid input. Please enter a valid number.')
            logger.info("User entered invalid input for habit selection.")

    while True:
        confirm = click.prompt(f"Are you sure you want to delete habit '{habit.name}'? [y/n]", type=str)
        if confirm.lower() in ('y', 'yes'):
            db.delete_habit(habit.name)
            click.echo(f"The habit '{habit.name}' was deleted from your list.")
            logger.info(f"Deleted {habit.name}")
            break
        elif confirm.lower() in ('n', 'no'):
            click.echo(f"The habit '{habit.name}' was not deleted from your list.")
            logger.info(f"The user canceled the deletion of the habit '{habit.name}'.")
            break
        else:
            click.echo("Invalid input. Please enter 'y' or 'n'.")
            logger.info(f"Invalid confirmation input: {confirm}")
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def habit_performed():
    """
    This function allows you to mark a habit as being performed the number of times equal to the periodicity
    that the user has chosen.
    """
    habits = db.show_all_habits()
    if not habits:
        click.echo('You don\'t have any habits created yet.')
        logger.info("There are no habits yet.")
        click.prompt('Press Enter to return to the main menu', default='', show_default=False)
        return

    click.echo('You have the following habits:')
    for x, habit in enumerate(habits, start=1):
        click.echo(f"{x}. {habit.name}")

    while True:
        try:
            choice = click.prompt('Select the habit you want to mark as done', type=int)
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                break
            else:
                click.echo('Please select a habit number from the list.')
                logger.info(f"User entered invalid input for habit selection.")
        except (ValueError, TypeError):
            click.echo('Please select a habit number from the list.')
            logger.info("User entered invalid input for habit selection.")

    if habit.can_mark_performed():
        habit.performed()
        db.add_completion(habit.name, habit.completion_dates[-1])
        click.echo(f"Great job! You've marked '{habit.name}' as completed.")
        logger.info(f"The habit '{habit.name}' was performed.")
    else:
        click.echo(f"You have already completed '{habit.name}' according to its periodicity")
        logger.info(f"The habit '{habit.name}' has completed the periodicity.")
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def all_habits():
    """
    This function displays a table of all habits, the table shows the name of the habit, its creation date,
    the frequency of the habit and its periodicity and also the date of the last time the habit was performed.
    """
    habits = db.show_all_habits()
    if not habits:
        click.echo('There are no habits created at the moment.')
        logger.info("No habits were recorded.")
        click.prompt('Press Enter to return to the main menu', default='', show_default=False)
        return
    analysis.table_of_habits(habits)
    logger.info("Show list of all habits.")
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def habits_frequency():
    """
    This function also displays a list with the same information as the all_habits function,
    but allows the user to filter habits according to their frequency.
    """
    frequency = click.prompt('Select the frequency of the habits you want to see',
                             type=click.Choice(['daily', 'weekly'], case_sensitive=False))
    habits = analysis.list_frequency(db, frequency.lower())
    if not habits:
        click.echo(f'No {frequency} habits found.')
        logger.info(f"There are no habits with the frequency '{frequency}'.")
        click.prompt('Press Enter to return to the main menu', default='', show_default=False)
        return
    analysis.table_of_habits(habits)
    logger.info(f"List of habits with the following frequency '{frequency}'.")
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def view_completion_dates():
    """
    This function allows the user to see the last seven completion dates of the habit they want to inspect.
    """
    habits = db.show_all_habits()
    if not habits:
        click.echo('There are no habits created at the moment.')
        logger.info("No habits were recorded.")
        click.prompt('Press Enter to return to the main menu', default='', show_default=False)
        return

    click.echo('Choose the habit you want to view completion dates for:')
    for x, habit in enumerate(habits, start=1):
        click.echo(f"{x}. {habit.name}")

    while True:
        try:
            choice = click.prompt('Choose the number of the habit', type=int)
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                break
            else:
                click.echo('Please select a habit number from the list.')
                logger.info(f"Invalid habit selection: {choice}")
        except (ValueError, TypeError):
            click.echo('Invalid input. Please enter a valid number.')
            logger.info("The user entered invalid input for habit selection.")

    analysis.display_completion_dates(habit)
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def view_current_streak():
    """
    This function shows the current streak of the habit that the user wants to inspect.
    """
    habits = db.show_all_habits()
    if not habits:
        click.echo('There are no habits created at the moment.')
        logger.info("No habits were recorded.")
        click.prompt('Press Enter to return to the main menu', default='', show_default=False)
        return

    click.echo('Choose the habit you want to check the current streak for:')
    for x, habit in enumerate(habits, start=1):
        click.echo(f"{x}. {habit.name}")

    while True:
        try:
            choice = click.prompt('Choose the number of the habit', type=int)
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                break
            else:
                click.echo('Please select a habit number from the list.')
                logger.info(f"Invalid habit selection: {choice}")
        except (ValueError, TypeError):
            click.echo('Invalid input. Please enter a valid number.')
            logger.info("The user entered invalid input for habit selection.")

    current_streak = habit.calculate_current_streak()
    click.echo(f"The current streak for habit '{habit.name}' is {current_streak}.")
    logger.info(f"The current streak '{current_streak}' for the habit '{habit.name}' was shown.")
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def specific_longest_streak():
    """
    This feature allows the user to see the longest streak they have achieved in a specific habit.
    """
    habits = db.show_all_habits()
    if not habits:
        click.echo('There are no habits created at the moment.')
        logger.info("No habits were recorded.")
        click.prompt('Press Enter to return to the main menu', default='', show_default=False)
        return

    click.echo('Choose the habit you want to check:')
    for x, habit in enumerate(habits, start=1):
        click.echo(f"{x}. {habit.name}")

    while True:
        try:
            choice = click.prompt('Choose the number of the habit you want to look at', type=int)
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                break
            else:
                click.echo('Please select a habit number from the list.')
                logger.info(f"Invalid habit selection: {choice}")
        except (ValueError, TypeError):
            click.echo('Invalid input. Please enter a valid number.')
            logger.info("The user entered invalid input for habit selection.")

    longest_streak = habit.calculate_longest_streak()
    click.echo(f"The longest streak for habit '{habit.name}' is {longest_streak}.")
    logger.info(f"The longest streak '{longest_streak}' for the habit '{habit.name}' was shown.")
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def longest_streak():
    """
    This feature allows the user to quickly check which habit has the longest streak among all habits.
    """
    habit = analysis.show_longest_streak(db)
    if habit:
        longest_streak = habit.calculate_longest_streak()
        click.echo(f"The habit with the longest streak is '{habit.name}', with a streak of {longest_streak}.")
        logger.info(f"The habit '{habit.name}' longest streak {longest_streak}.")
    else:
        click.echo('There are no habits created at the moment.')
        logger.info("No habits were recorded.")
    click.prompt('Press Enter to return to the main menu', default='', show_default=False)


def close_program():
    """
    This function allows the user to close the program.
    """
    db.exit()
    logger.info("The database was closed.")
    click.echo('Program finished, see you later!')
    click.echo('Remember success is not final, failure is not fatal. It is the courage to continue that counts.')
    sys.exit()


def main():
    """
    This function is the main function that runs the program, it provides the menu that the user interacts
    with to track their habits. It makes the program run in a loop until the user finishes the program.
    """
    logger.info("The program started.")
    while True:
        click.clear()
        click.echo('SIMPLE HABITS')
        click.echo('Options menu:')
        click.echo('1. Create habit')
        click.echo('2. Delete habit')
        click.echo('3. Mark habit as performed')
        click.echo('4. List of all currently tracked habits')
        click.echo('5. List of all habits with the same frequency')
        click.echo('6. View completion dates for a habit')
        click.echo('7. View current streak for a habit')
        click.echo('8. The longest run streak for a given habit')
        click.echo('9. The habit with the longest run streak of all defined habits')
        click.echo('10. Finish program')

        try:
            choice = click.prompt('What do you want to do?', type=int)
        except (ValueError, TypeError):
            click.echo('Please enter a number corresponding to the options.')
            logger.warning("The user entered invalid input in main menu.")
            continue

        if choice == 1:
            create_habit()
        elif choice == 2:
            delete_habit()
        elif choice == 3:
            habit_performed()
        elif choice == 4:
            all_habits()
        elif choice == 5:
            habits_frequency()
        elif choice == 6:
            view_completion_dates()
        elif choice == 7:
            view_current_streak()
        elif choice == 8:
            specific_longest_streak()
        elif choice == 9:
            longest_streak()
        elif choice == 10:
            close_program()
        else:
            click.echo('The selected option is not in the menu, please choose an option from the menu.')
            logger.warning(f"The user used an incorrect input")
            continue


if __name__ == '__main__':
    main()
