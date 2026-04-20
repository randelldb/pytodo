import os
import sqlite3


def main():
    conn = initDatabase()

    while True:
        menu(conn)

def menu(conn):
    clearConsole()
    print("[1] View tasks")
    print("[2] Add task")
    print("[3] Delete task")
    print("[X] Exit")

    choice = input("> ").strip()

    if choice == "1":
        listTasks(conn)
    elif choice == "2":
        addTask(conn)
    elif choice == "3":
        deleteTask(conn)
    elif choice == "X":
        exit()
    else:
        print("Faulty choice")


def addTask(conn):
    clearConsole()
    print("Add a task")
    taskInput = input()
    task = (taskInput, 0)

    sql = """
        INSERT INTO tasks(name, state)
            VALUES (?,?)
    """

    cursor = conn.cursor()
    cursor.execute(sql, task)
    conn.commit()

def listTasks(conn):
    clearConsole()
    print("Current tasks:")

    sql = """
        SELECT * FROM tasks
    """

    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        print(f"[{row[0]}] - {row[1]}")

    input("Press Enter to continue...")

def deleteTask(conn):
    clearConsole()
    listTasks(conn)

    print("Select a task to delete: ")
    taskId = input()

    sql = """
        DELETE FROM tasks WHERE id = ?
    """

    cursor = conn.cursor()
    cursor.execute(sql, taskId)
    conn.commit()

def initDatabase():
    sql = [
        """
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY,
                name text NOT NULL,
                state INTEGER 
            )
        """
    ]

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        for statement in sql:
            cursor.execute(statement)

        conn.commit()

        return conn
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
        return None

def clearConsole():
    print("\033[H\033[J", end="")

if __name__ == '__main__':
    main()
