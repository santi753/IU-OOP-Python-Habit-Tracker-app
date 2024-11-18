# Checking Your Habit Data with `database_check.py`

To ensure that the habit-tracking program meets the project requirement of having at least four weeks of data, we've provided a 
simple module called `database_check.py`. This module allows to view all the habits stored in your `habits.db` database.
The `database_check.py` module contains a function that connects to `habits.db` database and prints out all the habits.

## How to Use `database_check.py`

### 1. Download the Necessary Files

* **Module**: Download the `database_check.py` file from the repository.
* **Database File**: Download the `habits.db` database file. 

### 2. Place Files in the Same Folder

* Create a new folder on your computer.
* Place both `database_check.py` and `habits.db` into this folder. Keeping them in the same directory. 

### 3. Run the Module 

* **Open PowerShell**:
* **Navigate to the Folder**:
  * Use the `cd` command to change directories to the folder containing your files. For example:
    ```powershell
    cd C:\path\to\your\folder
    ```
* **Run the Script**:
  * To execute the script, type:
    ```powershell
    python database_check.py
    ```
