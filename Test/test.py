import pytest
from datetime import datetime, timedelta
from habit import Habit
from database import Database
import analysis
import os

# In this part of the tests, a @pytest.fixture is created, this fixture creates
# a temporary database for each test ensuring isolation.

@pytest.fixture
def test_db():
    """
    This fixture creates a temporary database to use in each test,
    and deletes it afterward so that each test runs independently.
    """
    test_db_name = 'test_habits.db'
    if os.path.exists(test_db_name):
        os.remove(test_db_name)
    db = Database(db_name=test_db_name, insert_predefined=False)
    yield db
    db.exit()
    if os.path.exists(test_db_name):
        os.remove(test_db_name)

# In this part of the tests, the Habit class and its methods are verified,
# since it is the fundamental part for the correct functioning of habit tracking.

def test_habit_creation_in_class():
    """
    This test evaluates how habits are created in the Habit class.
    """
    habit = Habit("Study", "daily", 1)
    assert habit.name == "Study"
    assert habit.frequency == "daily"
    assert habit.periodicity == 1
    assert isinstance(habit.creation_date, datetime)
    assert habit.completion_dates == []

def test_habit_performed():
    """
    This test checks that the performed() method correctly adds the current datetime to completion_dates.
    """
    test_habit = Habit(name="habit test", frequency="daily", periodicity=1)
    before_count = len(test_habit.completion_dates)
    test_habit.performed()
    after_count = len(test_habit.completion_dates)
    assert after_count == before_count + 1
    assert isinstance(test_habit.completion_dates[-1], datetime)

def test_can_mark_performed_daily():
    """
    This test checks the correct functioning of the can_mark_performed() method for daily habits.
    """
    test_habit = Habit(name="habit test 2", frequency="daily", periodicity=1)
    assert test_habit.can_mark_performed() == True
    test_habit.performed()
    assert test_habit.can_mark_performed() == False

def test_can_mark_performed_weekly():
    """
    This test checks the correct functioning of the can_mark_performed() method for weekly habits.
    """
    habit = Habit("habit test 3", "weekly", 2)
    assert habit.can_mark_performed() == True
    habit.performed()
    assert habit.can_mark_performed() == True
    habit.performed()
    assert habit.can_mark_performed() == False

def test_calculate_current_streak_daily():
    """
    This test checks the operation of the calculate_current_streak() method for daily habits.
    """
    habit = Habit("habit test 4", "daily", 1)
    today = datetime.now()

    for i in range(2, 0, -1):
        habit.completion_dates.append(today - timedelta(days=i))

    current_streak = habit.calculate_current_streak()
    assert current_streak == 2

    habit.completion_dates.append(today)
    current_streak = habit.calculate_current_streak()
    assert current_streak == 2

def test_calculate_current_streak_weekly():
    """
    This test checks the operation of the calculate_current_streak() method for weekly habits.
    """
    habit = Habit("habit test 5", "weekly", 1)
    today = datetime.now()

    for i in range(2, 0, -1):
        week_date = today - timedelta(weeks=i)
        habit.completion_dates.append(week_date)

    current_streak = habit.calculate_current_streak()
    assert current_streak == 2

    habit.completion_dates.append(today - timedelta(weeks=3))
    current_streak = habit.calculate_current_streak()
    assert current_streak == 3

def test_calculate_current_streak_with_pause_daily():
    """
    This test verifies the operation of the calculate_current_streak() method with a pause
    between completion dates for daily habits.
    """
    habit = Habit("habit test 6", "daily", 1)
    today = datetime.now()

    habit.completion_dates.append(today - timedelta(days=3))

    habit.completion_dates.append(today - timedelta(days=1))

    current_streak = habit.calculate_current_streak()
    assert current_streak == 1

def test_calculate_current_streak_with_pause_weekly():
    """
    This test verifies the operation of the calculate_current_streak() method with a pause
    between completion dates for weekly habits.
    """
    habit = Habit("habit test 7", "weekly", 1)
    today = datetime.now()

    habit.completion_dates.append(today - timedelta(weeks=3))
    habit.completion_dates.append(today - timedelta(weeks=1))

    current_streak = habit.calculate_current_streak()
    assert current_streak == 1

def test_calculate_longest_streak_daily(test_db):
    """
    This test verifies that the calculate_longest_streak() method works correctly for daily habits.
    """
    habit = Habit("habit test 8", "daily", 1)
    test_db.new_created_habit(habit)

    today = datetime.now()

    for i in range(6, 3, -1):
        test_db.add_completion(habit.name, today - timedelta(days=i))

    for i in range(2, 0, -1):
        test_db.add_completion(habit.name, today - timedelta(days=i))

    longest_streak = analysis.longest_streak_for_habit(test_db, habit.name)
    assert longest_streak == 3

def test_calculate_longest_streak_weekly():
    """
    This test verifies that the calculate_longest_streak() method works correctly for weekly habits.
    """
    habit = Habit("habit test 9", "weekly", 1)
    today = datetime.now()

    for i in range(6, 3, -1):
        habit.completion_dates.append(today - timedelta(weeks=i))

    for i in range(2, 0, -1):
        habit.completion_dates.append(today - timedelta(weeks=i))

    longest_streak = habit.calculate_longest_streak()
    assert longest_streak == 3

# In this part, it is verified that the program database is created correctly
# since it is key to the operation of the program.

def test_database_creation(test_db):
    """
    This test checks that the database with the required tables has been created.
    """
    assert os.path.exists(test_db.db_name)
    test_db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = test_db.cursor.fetchall()
    assert len(tables) >= 2

# In this part, the operation of the main functions of the program menu is verified,
# which the user will use to interact with the program.

def test_new_habit_creation(test_db):
    """
    This test checks the creation of a new habit.
    """
    test_habit = Habit(name="habit test", frequency="daily", periodicity=1)
    test_db.new_created_habit(test_habit)
    habit = test_db.find_habit(test_habit.name)
    assert habit is not None
    assert habit.name == test_habit.name
    assert habit.frequency == test_habit.frequency
    assert habit.periodicity == test_habit.periodicity

def test_delete_habit(test_db):
    """
    This test checks the deletion of a habit from the program.
    """
    test_habit = Habit(name="habit test 2", frequency="daily", periodicity=1)
    test_db.new_created_habit(test_habit)
    test_db.delete_habit(test_habit.name)
    habit = test_db.find_habit(test_habit.name)
    assert habit is None

def test_show_all_habits(test_db):
    """
    This test checks that the list of habits is shown to the user when requested.
    """
    habits = [
        Habit("habit test 3", "daily", 1),
        Habit("habit test 4", "weekly", 2),
        Habit("habit test 5", "daily", 3)
    ]
    for habit in habits:
        test_db.new_created_habit(habit)

    all_habits = test_db.show_all_habits()
    assert len(all_habits) == 3
    assert all(isinstance(h, Habit) for h in all_habits)

def test_show_frequency(test_db):
    """
    This test checks that the list of habits with the specified frequency is shown to
    the user when requested.
    """
    habits = [
        Habit("habit test 6", "daily", 1),
        Habit("habit test 7", "weekly", 1),
        Habit("habit test 8", "daily", 2),
    ]
    for habit in habits:
        test_db.new_created_habit(habit)

    daily_habits = test_db.show_frequency("daily")
    assert len(daily_habits) == 2
    assert all(h.frequency == "daily" for h in daily_habits)

def test_view_completion_dates():
    """
    This test checks that the completion dates of a habit can be retrieved and displayed correctly.
    """
    habit = Habit("habit test 9", "daily", 1)
    today = datetime.now()

    completion_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    habit.completion_dates.extend(completion_dates)

    last_seven_dates = sorted(habit.completion_dates)[-7:]
    assert len(last_seven_dates) == 7
    assert last_seven_dates == completion_dates

def test_view_current_streak():
    """
    This test checks that the current streak of a habit is calculated correctly.
    """
    habit = Habit("habit test 10", "daily", 1)
    today = datetime.now()

    for i in range(2, 0, -1):
        habit.completion_dates.append(today - timedelta(days=i))

    habit.completion_dates.append(today)

    current_streak = habit.calculate_current_streak()
    assert current_streak == 2

def test_longest_streak_for_habit_daily(test_db):
    """
    This test verifies that the user can see the longest streak achieved for a specific habit.
    """
    habit = Habit("habit test 11", "daily", 1)
    test_db.new_created_habit(habit)

    today = datetime.now()

    for i in range(6, 3, -1):
        test_db.add_completion(habit.name, today - timedelta(days=i))

    for i in range(2, 0, -1):
        test_db.add_completion(habit.name, today - timedelta(days=i))

    longest_streak = analysis.longest_streak_for_habit(test_db, habit.name)
    assert longest_streak == 3

def test_longest_streak_for_habit_weekly(test_db):
    """
    This test verifies that the user can see the longest streak achieved for a specific weekly habit.
    """
    habit = Habit("habit test 12", "weekly", 1)
    test_db.new_created_habit(habit)

    today = datetime.now()

    for i in range(6, 3, -1):
        test_db.add_completion(habit.name, today - timedelta(weeks=i))

    for i in range(2, 0, -1):
        test_db.add_completion(habit.name, today - timedelta(weeks=i))

    longest_streak = analysis.longest_streak_for_habit(test_db, habit.name)
    assert longest_streak == 3

def test_longest_streak(test_db):
    """
    This test verifies that the program finds the longest streak among all habits for the user.
    """

    habit1 = Habit("habit test 13", "daily", 1)
    habit2 = Habit("habit test 14", "daily", 1)
    habit3 = Habit("habit test 15", "weekly", 1)
    test_db.new_created_habit(habit1)
    test_db.new_created_habit(habit2)
    test_db.new_created_habit(habit3)

    today = datetime.now()

    for i in range(3, 0, -1):
        test_db.add_completion(habit1.name, today - timedelta(days=i))

    for i in range(5, 0, -1):
        test_db.add_completion(habit2.name, today - timedelta(days=i))

    for i in range(4, 0, -1):
        test_db.add_completion(habit3.name, today - timedelta(weeks=i))

    longest_streak_habit = analysis.show_longest_streak(test_db)
    assert longest_streak_habit is not None
    assert longest_streak_habit.name == habit2.name
    assert longest_streak_habit.calculate_longest_streak() == 5
