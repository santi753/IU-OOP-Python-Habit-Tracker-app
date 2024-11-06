# Simple Habits - Habit Tracking Application

A Python-based habit tracking application that helps users create, maintain, and analyze their daily and weekly habits. This application was developed as part of the Object-Oriented Programming course at IU International University.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Required Packages](#required-packages)
   - [Setup](#setup)
3. [Usage](#usage)
   - [Example Usage](#example-usage)
4. [Project Structure](#project-structure)
   - [Core Files](#core-files)
   - [Additional Files](#additional-files)
5. [Testing](#testing)
   - [Running Tests](#running-tests)
   - [Test Coverage](#test-coverage)
   - [Test Database](#test-database)
6. [Contributing](#contributing)
7. [License](#license)

## Features

- Create and delete habits with customizable frequencies (daily/weekly)
- Track habit completion with built-in periodicity checks
- View all currently tracked habits in a formatted table
- Filter habits by frequency (daily/weekly)
- View completion dates for specific habits
- Track current and longest streaks for each habit
- Find the habit with the longest streak
- Command-line interface for easy interaction
- SQLite database for persistent storage
- Comprehensive logging system

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Required Packages
The following Python packages are required to run the application:

- datetime
- collections
- logging
- sqlite3
- tabulate
- click
- pytest
- os
- sys

### Setup

1. Clone the repository  
   - `git clone https://github.com/santi753/IU-OOP-Python-Habit-Tracker-app.git`

2. Navigate to the project directory  
   - `cd IU-OOP-Python-Habit-Tracker-app/Simple Habits`

3. Install the required packages  
   - `pip install -r requirements.txt`

4. Run the application  
   - `python main.py`

## Usage

When you run the application, you'll be presented with a menu-driven interface offering the following options:

1. **Create habit**
   - Name your new habit
   - Choose frequency (daily/weekly)
   - Set periodicity (how many times per day/week)

2. **Delete habit**
   - Select a habit from your list to remove it
   - Confirmation required before deletion

3. **Mark habit as performed**
   - Select a habit to mark as complete
   - System checks if marking is allowed based on periodicity
   - Automatic tracking of completion dates

4. **View your habits**
   - List all currently tracked habits
   - See creation dates
   - View frequency and periodicity
   - Check last completion date

5. **Analyze habits**
   - Filter habits by frequency (daily/weekly)
   - View completion dates for specific habits
   - Check current streaks
   - See longest streaks
   - Find your most consistent habit

### Example Usage

To create a new habit:
1. Select option 1 from the main menu
2. Enter habit name (e.g., "Morning Exercise")
3. Choose frequency ("daily" or "weekly")
4. Set periodicity (e.g., 3 times per week)

## Project Structure

The project follows an object-oriented design with the following main components:

### Core Files

- **main.py**
  - Main program entry point
  - Command-line interface implementation
  - Menu-driven user interaction
  - Program flow control

- **habit.py**
  - `Habit` class implementation
  - Core functionality for habit management
  - Streak calculation methods
  - Completion tracking logic

- **database.py**
  - `Database` class for data persistence
  - SQLite database management
  - CRUD operations for habits
  - Completion date storage

- **analysis.py**
  - Habit analysis functions
  - Data visualization (table format)
  - Streak calculations
  - Filtering capabilities

- **test.py**
  - Comprehensive test suite
  - Unit tests for all core functionality
  - Database testing
  - Streak calculation verification

### Additional Files

- **habits.db**
  - SQLite database file
  - Stores habit data and completion records
  - Created automatically on first run

- **habit_tracker.log**
  - Logging file
  - Tracks program operations
  - Records user actions and system events

## Testing

The application includes a comprehensive test suite using pytest to ensure reliability and correct functionality.

### Running Tests

To run all tests:
- `pytest test.py`

To run tests with detailed output:
- `pytest -v test.py`

### Test Coverage

The test suite covers:

1. **Habit Class Testing**
   - Habit creation
   - Frequency validation
   - Periodicity checking
   - Completion date tracking
   - Streak calculations (daily and weekly)

2. **Database Testing**
   - Database creation and connection

3. **Analysis Testing**
   - Habit filtering
   - Data presentation

4. **Integration Testing**
   - Data consistency
   - User operation sequences

### Test Database

Tests use a separate test database (`test_habits.db`) to ensure:
- Isolation from production data
- Clean testing environment
- No interference with user data
- Automatic cleanup after testing

## Contributing

This project is open source and contributions are welcome. 

## License

This project is licensed under the MIT License.

MIT License

Copyright (c) 2024 santi753




   

