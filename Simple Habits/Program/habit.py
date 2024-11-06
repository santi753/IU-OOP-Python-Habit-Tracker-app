# habit.py

import logging
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class Habit:
    """
    A class for each habit creation.

    Attributes:
        name (str): the name of the habit.
        frequency (str): how often the habit should be performed ('daily' or 'weekly').
        periodicity (int): the number of times the habit should be performed in the given frequency period.
        creation_date (datetime): when the habit was created.
        completion_dates (list): list of the dates when the habit was completed.
    """

    def __init__(self, name: str, frequency: str, periodicity: int):
        """
        Initialize a new habit.

        Args:
            name (str): the name of the habit.
            frequency (str): how often the habit should be performed, daily or weekly.
            periodicity (int): the number of times the habit should be performed in the given frequency period.
        """
        self.name = name
        self.frequency = frequency.lower()
        self.periodicity = periodicity
        self.creation_date = datetime.now()
        self.completion_dates = []

    def performed(self):
        """
        This method marks the habit as completed at the current date.
        It adds the current date to the list of completion dates.
        """
        now = datetime.now()
        self.completion_dates.append(now)
        logger.info(f"The habit '{self.name}' was performed at {now}.")

    def can_mark_performed(self):
        """
        This method will check if the user can mark the habit or not depending on the periodicity of the habit.

        Returns:
            bool: it will be true if the habit can still be marked since the periodicity has not been reached,
            and false if the habit has already been marked the necessary number of times.
        """

        now = datetime.now()

# In the method a period is created to calculate the number of times the user has performed the habit, checking the frequency.
        if self.frequency == 'daily':
            period_start = datetime(now.year, now.month, now.day)
            period_end = period_start + timedelta(days=1)
        # For daily habits, it calculates the start of the current period by creating a variable with the date set to midnight of today
        # and then it sets the end of the period to the start of the next day by adding one day.

        elif self.frequency == 'weekly':
            period_start = datetime(now.year, now.month, now.day) - timedelta(days=now.weekday())
            period_end = period_start + timedelta(weeks=1)
        # For weekly habits, the most recent monday is found by subtracting the number of days from monday to the current date
        # and then setting the end of the period to the beginning of the following week by adding one week.
        else:
            raise ValueError(f"The frequency is not correct '{self.frequency}'. The frequency should be daily or weekly.")

# The method then counts how many times you have marked the habit as done during the current period.
# It uses the list to iterate through all the completion dates and counts the dates that fall within the period you set at the beginning.
        count = sum(1 for date in self.completion_dates if period_start <= date < period_end)

# Finally, it returns true if the count is less than the required periodicity, allowing the habit to continue being marked,
# and false otherwise, not allowing the habit to be marked since the user has marked the habit the number of times proposed.
        return count < self.periodicity

    def calculate_current_streak(self):
        """
        Calculate the current streak of the habit.

        Returns:
            int: the current streak count, returns 0 if there is no streak.
        """
# First, the method checks if the habit has been completed yet
        if not self.completion_dates:
            return 0

# After the method orders the completion dates in ascending order, which will make it easier to analyze the consecutive periods
# in which the habit was performed.
        sorted_dates = sorted(self.completion_dates)

# Within the method, The duration of the period is defined based on the frequency of the habit
# and a function period_start to calculate the start of each period depending on the frequency of the habit
# to group the completion dates.
        if self.frequency == 'daily':
            duration = timedelta(days=1)
            period_start = lambda d: datetime(d.year, d.month, d.day)
        # For daily habits the period duration is one day, and period_start returns the start of the day
        # using the midnight for any date in completion dates.
        elif self.frequency == 'weekly':
            duration = timedelta(weeks=1)
            period_start = lambda d: datetime(d.year, d.month, d.day) - timedelta(days=d.weekday())
        # For weekly habits, the period duration is one week and period_start returns the start of the week with monday
        # at midnight for any date in completion dates.
        else:
            raise ValueError(f"The frequency is not correct '{self.frequency}'. The frequency should be daily or weekly.")

# Now the period_start of each date is placed in the period_counts dictionary as a key, the value of these keys
# will be the count of how many times the habit was performed in that period.
        period_counts = defaultdict(int)
        for date in sorted_dates:
            period = period_start(date)
            period_counts[period] += 1

# Then we create a set, in which the method will iterate through the dictionary periods and it will only keep the dates
# that meet the periodicity required for each habit.
        eligible_periods = set(period for period, count in period_counts.items() if count == self.periodicity)

# Here the method creates the variables needed to start calculating the current streak by setting the expected_period
# to last_period, the period immediately preceding the current period. And then starting the current_streak at zero.
        now = datetime.now()
        current_period = period_start(now)
        last_period = current_period - duration
        expected_period = last_period
        current_streak = 0

# Then the method uses a loop with the variable expected_period and the set eligible_periods, in which it is checked that
# the expected period is in the set of eligible periods, if so, the duration of the corresponding period is subtracted
# from the expected period and the streak is increased by one. The verification is done retrospectively
# It continues in this way until the expected period is no longer among the eligible periods, the loop ends.
        while expected_period in eligible_periods:
            current_streak += 1
            expected_period -= duration

#Finally when the loop ends, the method returns the current streak
        return current_streak

    def calculate_longest_streak(self):
        """
        Calculate the longest streak achieved for this habit.

        Returns:
            int: the longest streak achieved in the habit.
        """
# First, the method checks if the habit has been completed yet
        if not self.completion_dates:
            return 0

# After the method orders the completion dates in ascending order, which will make it easier to analyze the consecutive periods
# in which the habit was performed.
        sorted_dates = sorted(self.completion_dates)

# Within the method, The duration of the period is defined based on the frequency of the habit
# and a function period_start to calculate the start of each period depending on the frequency of the habit
# to group the completion dates.
        if self.frequency == 'daily':
            duration = timedelta(days=1)
            period_start = lambda d: datetime(d.year, d.month, d.day)
        # For daily habits the period duration is one day, and period_start returns the start of the day
        # using the midnight for any date in completion dates.
        elif self.frequency == 'weekly':
            duration = timedelta(weeks=1)
            period_start = lambda d: datetime(d.year, d.month, d.day) - timedelta(days=d.weekday())
        # For weekly habits, the period duration is one week and period_start returns the start of the week with monday
        # at midnight for any date in completion dates.
        else:
            raise ValueError(f"The frequency is not correct '{self.frequency}'. The frequency should be daily or weekly.")

# Now the period_start of each date is placed in the period_counts dictionary as a key, the value of these keys
# will be the count of how many times the habit was performed in that period.
        period_counts = defaultdict(int)
        for date in sorted_dates:
            period = period_start(date)
            period_counts[period] += 1

# Then, the method creates the variables to start calculating the longest streak, sort the periods,
# and set initial values for the current longest streak, and the previous period.
        sorted_periods = sorted(period_counts.keys())
        longest_streak = 0
        current_streak = 0
        previous_period = None

# After that, the method iterate through each period and checks whether the completion count
# meets the required periodicity. If so, it checks whether the periods are consecutive
# and updates the current and longest streaks.
        for period in sorted_periods:
            count = period_counts[period]
            if count == self.periodicity:
                if previous_period is None:
                    current_streak = 1
                else:
                    if period - previous_period == duration:
                        current_streak += 1
                    else:
                        current_streak = 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 0
            previous_period = period

# Finally returns the longest streak of the desired habit.
        return longest_streak

